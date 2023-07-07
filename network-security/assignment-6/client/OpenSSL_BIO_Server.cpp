#include "OpenSSL_BIO_Server.h"

#include <arpa/inet.h>
#include <asm-generic/socket.h>
#include <cstdlib>
#include <cstring>
#include <netinet/in.h>
#include <openssl/bio.h>
#include <openssl/err.h>
#include <openssl/ssl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>

OpenSSL_BIO_Server::OpenSSL_BIO_Server(){};
OpenSSL_BIO_Server::~OpenSSL_BIO_Server(){};

void OpenSSL_BIO_Server::createSocket(int port) {
  serverSocket = socket(AF_INET, SOCK_STREAM, 0);

  if (serverSocket < 0) {
    perror("Unable to create socket");
    exit(EXIT_FAILURE);
  }

  serverAddress.sin_family = AF_INET;
  serverAddress.sin_port = htons(port);
  serverAddress.sin_addr.s_addr = htonl(INADDR_ANY);

  int optval = 1;
  setsockopt(serverSocket, SOL_SOCKET, SO_REUSEPORT, &optval, sizeof(optval));

  if (bind(serverSocket, (struct sockaddr *)&serverAddress,
           sizeof(serverAddress) < 0)) {
    perror("Unable to bind socket");
    exit(EXIT_FAILURE);
  }

  if (listen(serverSocket, 1) < 0) {
    perror("Listen on socket failed");
    exit(EXIT_FAILURE);
  }
}

void OpenSSL_BIO_Server::waitForIncomingConnection() {
  printf("Waiting for incoming connection...");
  unsigned int clientAddressLen = sizeof(clientAddress);
  clientSocket = accept(serverSocket, (struct sockaddr *)&clientAddress,
                        &clientAddressLen);

  if (clientSocket < 0) {
    perror("Accept on socket failed");
  }
  printf("Connection accepted!");

  doSSLHandshake();
}

void OpenSSL_BIO_Server::doSSLHandshake() {
  char buffer[BUFFERSIZE];

  int recievedBytes = read(clientSocket, buffer, BUFFERSIZE);

  while (!SSL_is_init_finished(ssl)) {
    SSL_do_handshake(ssl);

    int bytesToWrite = BIO_read(writeBIO, buffer, BUFFERSIZE);

    if (bytesToWrite > 0) {
      printf("Host has %d bytes of encrypted data to send", bytesToWrite);
      write(clientSocket, buffer, bytesToWrite);
    } else {
      int receivedBytes = read(clientSocket, buffer, BUFFERSIZE);
      if (receivedBytes > 0) {
        printf("Host has received %d bytes", receivedBytes);
        BIO_write(readBIO, buffer, receivedBytes);
      }
    }
    printf("Host SSL Handshake done!");
  }
}

char *OpenSSL_BIO_Server::readFromSocket() {
  char *buffer[BUFFERSIZE];

  int receivedBytes = read(clientSocket, buffer, BUFFERSIZE);
  if (receivedBytes > 0) {
    printf("Host has received %d bytes of encrypted data", receivedBytes);
    BIO_write(readBIO, buffer, receivedBytes);
  }

  int sizeUnencryptedBytes = SSL_read(ssl, buffer, receivedBytes);
  if (sizeUnencryptedBytes < 0) {
    perror("SSL_read() failed");
    exit(EXIT_FAILURE);
  }

  char *msg = new char[sizeUnencryptedBytes];
  memcpy(msg, buffer, sizeUnencryptedBytes);

  return msg;
}

void OpenSSL_BIO_Server::initOpenSSL() {
  SSL_load_error_strings();
  OpenSSL_add_ssl_algorithms();

  context = createContext();
  configureContext(context);

  ssl = SSL_new(context);
  readBIO = BIO_new(BIO_s_mem());
  writeBIO = BIO_new(BIO_s_mem());

  SSL_set_bio(ssl, readBIO, writeBIO);
  SSL_set_accept_state(ssl);
}
