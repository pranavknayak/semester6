#pragma once

#include <netinet/in.h>

struct ssl_ctx_st;
struct ssl_st;
struct bio_st;
typedef struct ssl_ctx_st SSL_CTX;
typedef struct ssl_st SSL;
typedef struct bio_st BIO;

class OpenSSL_BIO_Server {
public:
  OpenSSL_BIO_Server();
  virtual ~OpenSSL_BIO_Server();

  void createSocket(int port);
  void waitForIncomingConnection();
  char *readFromSocket();
  void closeSocket();

  void initOpenSSL();
  void cleanupOpenSSL();
  SSL_CTX *createContext();
  void configureContext(SSL_CTX *ctx);
  void doSSLHandshake();

private:
  int serverSocket;
  int clientSocket;
  struct sockaddr_in serverAddress;
  struct sockaddr_in clientAddress;

  SSL *ssl;
  SSL_CTX *context;
  BIO *readBIO;
  BIO *writeBIO;

  const int BUFFERSIZE = 1024;
  const char *CERT_FILE = "/home/fuji/Desktop/sem-6/network-security/"
                          "assignment-6/task1/certificates/root.crt";
  const char *KEY_FILE = "/home/fuji/Desktop/sem-6/network-security/"
                         "assignment-6/task1/keys/rootKey.pem";
};
