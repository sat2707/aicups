QT += core network
QT -= gui

CONFIG += c++11

TARGET = cpp11_client
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

SOURCES += main.cpp

HEADERS += \
    core/api.h \
    core/base_strategy.h \
    core/client.h \
    core/strategy.h
