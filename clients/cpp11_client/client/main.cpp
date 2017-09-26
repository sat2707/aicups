#include <QCoreApplication>
#include "core/client.h"
#include "core/api_elevators.h"
#include <cstdlib>
#include <QHostInfo>

#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>

int lookup_host(const char* host, char* addrstr) {
    struct addrinfo hints, *res;
    int errcode;
    void *ptr;

    memset(&hints, 0, sizeof (hints));
    hints.ai_family = PF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags |= AI_CANONNAME;

    errcode = getaddrinfo(host, NULL, &hints, &res);
    if (errcode != 0) {
        return -1;
    }
    printf("Host: %s\n", host);
    while (res) {
        inet_ntop(res->ai_family, res->ai_addr->sa_data, addrstr, 100);

        switch (res->ai_family) {
        case AF_INET:
            ptr = &((struct sockaddr_in *) res->ai_addr)->sin_addr;
            break;
        case AF_INET6:
            ptr = &((struct sockaddr_in6 *) res->ai_addr)->sin6_addr;
            break;
        }
        inet_ntop(res->ai_family, ptr, addrstr, 100);
        printf("IPv%d address: %s (%s)\n", res->ai_family == PF_INET6 ? 6 : 4, addrstr, res->ai_canonname);
        res = res->ai_next;
    }
    return 0;
}


int main(int argc, char *argv[])
{
    QString host = "127.0.0.1";
    int solution_id = 1, port = 8000;
    const char* env_value;
    char host_ip[100];

    if ((env_value = std::getenv("WORLD_NAME"))) {
        if (lookup_host(env_value, host_ip) == 0) {
            host = QString(host_ip);
        }
        else {
            std::cout << "Can't determine host" << std::endl;
        }
    }
    if ((env_value = std::getenv("SOLUTION_ID"))) {
        solution_id = QString(env_value).toInt();
    }

    QCoreApplication app(argc, argv);
    Client client(host, port, solution_id);
    API_Elevators api;

    QObject::connect(&client, SIGNAL(received(QJsonObject)), &api, SLOT(generateActions(QJsonObject)));
    QObject::connect(&api, SIGNAL(sendActions(QJsonArray)), &client, SLOT(sendActions(QJsonArray)));
    QObject::connect(&client, SIGNAL(finished()), &app, SLOT(quit()));

    client.start();
    return app.exec();
}
