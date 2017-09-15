#ifndef CLIENT_H
#define CLIENT_H

#include <QTcpSocket>
#include <QDataStream>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <iostream>


class Client : public QObject
{
    Q_OBJECT

private:
    QTcpSocket *socket;
    QString host;
    QString readData;
    int port;
    int solution_id;
    bool transmitting;

public:
    Client(const QString& _host, int _port, int _solution_id)
        : host(_host), port(_port), solution_id(_solution_id), transmitting(false)
    {
        socket = new QTcpSocket(this);
    }
    ~Client() {
        if (socket) delete socket;
    }

    void start() {
        connect(socket, SIGNAL(connected()), SLOT(slotConnected()));
        connect(socket, SIGNAL(readyRead()), SLOT(slotReadyRead()));
        connect(socket, SIGNAL(error(QAbstractSocket::SocketError)), this, SLOT(slotError(QAbstractSocket::SocketError)));
        readData = "";
        socket->connectToHost(host, port);
    }

private slots:
    void slotConnected() {
        QString greeting = "{\"solution_id\": " + QString::number(solution_id) + "}\n";
        int sent = socket->write(greeting.toStdString().c_str());
        if (sent == 0) {
            std::cout << "Can not send solution_id" << std::endl;
        }
    }

    void slotReadyRead() {
        if (socket->bytesAvailable() > 0) {
            QString data(socket->readAll());
            readData += data;

            int end_marker;
            QJsonParseError parseError;
            while ((end_marker = readData.indexOf("\n", 0)) != -1) {
                QString forJson = readData.left(end_marker);
                QJsonDocument json = QJsonDocument::fromJson(forJson.toUtf8(), &parseError);
                readData = readData.mid(end_marker + 1);

                if (! json.isObject() || parseError.error != QJsonParseError::NoError) {
                    std::cout << "Can not parse json: " << readData.toStdString() << std::endl;
                    std::cout << parseError.errorString().toStdString() << std::endl;
                }
                else {
                    handleJson(json.object());
                }
            }
        }
    }

    void handleJson(const QJsonObject & jsonData) {
        if (jsonData.value("message").toString("") == "down") {
            std::cout << "Parsed down" << std::endl;
            transmitting = false;
            socket->disconnectFromHost();
            emit finished();
        }
        if (transmitting) {
            emit received(jsonData);
        }
        if (jsonData.value("message").toString("") == "beginning") {
            std::cout << "Parsed beginning" << std::endl;
            transmitting = true;
        }
    }

    void sendActions(QJsonArray actions) {
//        QJsonObject jsonData;
//        jsonData.insert("turn", QJsonValue(actions));
        QJsonDocument json(actions);

        QString message = QString(json.toJson(QJsonDocument::Compact)) + "\n";
        int sent = socket->write(message.toStdString().c_str());
        if (sent == 0) {
            std::cout << "Can not send turn" << std::endl;
        }
    }

    void slotError(QAbstractSocket::SocketError error) {
        std::cout << "Socket error: " << error << std::endl;
    }

signals:
    void received(QJsonObject data);
    void finished();
};

#endif // CLIENT_H
