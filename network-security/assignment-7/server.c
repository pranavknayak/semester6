#include <arpa/inet.h>
#include <netinet/in.h>
#include <openssl/err.h>
#include <openssl/ssl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int create_socket(int port) {
  int s;
  struct sockaddr_in addr;

  addr.sin_family = AF_INET;
  addr.sin_port = htons(port);
  addr.sin_addr.s_addr = htonl(INADDR_ANY);

  s = socket(AF_INET, SOCK_STREAM, 0);
  if (s < 0) {
    perror("Unable to create socket");
    exit(EXIT_FAILURE);
  }

  if (bind(s, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
    perror("Unable to bind socket");
    exit(EXIT_FAILURE);
  }

  if (listen(s, 1) < 0) {
    perror("Unable to listen");
  }

  return s;
}

SSL_CTX *create_context() {
  const SSL_METHOD *method;
  SSL_CTX *ctx;

  method = TLS_server_method();

  ctx = SSL_CTX_new(method);
  if (!ctx) {
    perror("Unable to create context");
    ERR_print_errors_fp(stderr);
    exit(EXIT_FAILURE);
  }
  return ctx;
}

void configure_context(SSL_CTX *ctx) {
  if (SSL_use_certificate_file(ctx, "./task1/certificates/bob.crt",
                               SSL_FILETYPE_PEM) <= 0) {
    ERR_print_errors_fp(stderr);
    exit(EXIT_FAILURE);
  }
  if (SSL_use_RSAPrivateKey_file(ctx, "./task1/keys/bobKey.pem",
                                 SSL_FILETYPE_PEM) <= 0) {
    ERR_print_errors_fp(stderr);
    exit(EXIT_FAILURE);
  }
}

int main() {
  int sock;
  SSL_CTX *ctx;

  signal(SIGPIPE, SIG_IGN);

  ctx = create_context();
  configure_context(ctx);

  sock = create_socket(4433);

  while (1) {
    struct sockaddr_in addr;
    unsigned int len = sizeof(addr);
    SSL *ssl;
    const char reply[] = "test\n";

    int client = accept(sock, (struct sockaddr *)&addr, &len);
    if (client < 0) {
      perror("Unable to accept");
      exit(EXIT_FAILURE);
    }

    ssl = SSL_new(ctx);
    SSL_set_fd(ssl, client);

    if (SSL_accept(ssl) <= 0) {
      ERR_print_errors_fp(stderr);
    } else {
      SSL_write(ssl, reply, strlen(reply));
    }
    SSL_shutdown(ssl);
    SSL_free(ssl);
    close(client);
  }

  close(sock);
  SSL_CTX_free(ctx);
}
