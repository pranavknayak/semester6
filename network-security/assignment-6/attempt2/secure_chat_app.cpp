#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <openssl/err.h>
#include <openssl/ssl.h>
#include <openssl/x509_vfy.h>
#include <sys/socket.h>

int verify_callback(int preverify_ok, X509_STORE_CTX *ctx) {
  SSL *ssl = (SSL *)X509_STORE_CTX_get_ex_data(
      ctx, SSL_get_ex_data_X509_STORE_CTX_idx());

  X509 *cert = X509_STORE_CTX_get_current_cert(ctx);

  if (preverify_ok == 0) {
    return 0;
  } else {
    return 1;
  }
}

int main() {
  SSL_CTX *ctx;
  SSL *ssl;
  int sockfd;

  ctx = SSL_CTX_new(TLS_method());

  /*
   * Set up certificate store and chain verification below
   */

  X509_STORE *store = X509_STORE_new();
  if (store == NULL) {
    perror("Error creating a trust store");
  }

  if (X509_STORE_load_locations(store, "../task1/certificates/root.crt",
                                NULL) != 1) {
    perror("Error loading Root CA into store");
  }

  if (X509_STORE_load_locations(store, "../task1/certificates/int.crt", NULL) !=
      1) {
    perror("Error loading Intermediate CA into store");
  }

  SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, verify_callback);

  SSL_CTX_set_cert_store(ctx, store);

  /*
   * Set up certificate store and chain verification above
   */

  if (!ctx) {
    perror("Error creating context");
    exit(EXIT_FAILURE);
  }

  ssl = SSL_new(ctx);
  if (!ssl) {
    perror("Error creating SSL object");
    exit(EXIT_FAILURE);
  }

  sockfd = socket(AF_INET, SOCK_STREAM, 0);

  SSL_set_fd(ssl, sockfd);

  X509 *cert = SSL_get_peer_cert_chain(ssl);
  if (cert == NULL) {
    perror("Error accessing peer certificate");
  }
}
