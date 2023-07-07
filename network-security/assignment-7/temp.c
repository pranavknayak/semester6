#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <string.h>

int main() {
  char ip[INET_ADDRSTRLEN] = "";
  char addr[200] = "192.168.1.1";
  struct sockaddr_in *mystruct;

  inet_pton(AF_INET, addr, &mystruct);
  inet_ntop(AF_INET, &mystruct, ip, INET_ADDRSTRLEN);
  printf("\n\nIP Address: %s\n\n", ip);
  return 0;
}
