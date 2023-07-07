#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <string.h>

int main() {
  struct sockaddr_in my_struct;
  struct hostent *host_ent;

  host_ent = gethostbyname("www.google.com");
  bcopy()
}
