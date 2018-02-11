/*
 *    pinger.c 
 *    This is a ping imitation program 
 *    It will send an ICMP ECHO packet to the server of 
 *    your choice and listen for an ICMP REPLY packet
 *    Have fun!
 */
/*
 *    pinger.c 
 *    This is a ping imitation program 
 *    It will send an ICMP ECHO packet to the server of 
 *    your choice and listen for an ICMP REPLY packet
 *    Have fun!
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
/*
#include <linux/ip.h>
#include <linux/icmp.h>
#include <linux/tcp.h>
*/
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <netinet/tcp.h>
 

struct tcp_pseudo_hdr
{
    u_int32_t source_address;
    u_int32_t dest_address;
    u_int8_t placeholder;
    u_int8_t protocol;
    u_int16_t tcp_length;
};
char dst_addr[15];
char src_addr[15];
 
unsigned short in_cksum(unsigned short *, int);
void parse_argvs(char**, char*, char* );
void usage();
char* getip();
char* get_dummy_data();

 
int main(int argc, char* argv[])
{
    struct iphdr  *ip, *ip2;
    struct iphdr *ip_reply;
    struct icmphdr *icmp;
	struct tcphdr *tcp;
	struct tcp_pseudo_hdr phdr;
    struct sockaddr_in connection;
    char* packet;
	char packet2[4096];
    char* buffer;
	char buffer2[4096];
    char* pseudogram;
	char *data;
	int sockfd;
	int sockfd2;
    int optval = 1;
    int addrlen;
     
    if (getuid() != 0) {
    	fprintf(stderr, "%s: root privelidges needed\n", *(argv + 0));
    	exit(EXIT_FAILURE);
    }
 
    parse_argvs(argv, dst_addr, src_addr);
    printf("Source address: %s\n", src_addr);
    printf("Destination address: %s\n", dst_addr);
     
    /*
     * allocate all necessary memory
    */
    ip = malloc(sizeof(struct iphdr));
    ip2 = malloc(sizeof(struct iphdr));
    ip_reply = malloc(sizeof(struct iphdr));
    icmp = malloc(sizeof(struct icmphdr));
	tcp = malloc(sizeof(struct tcphdr));	// @gar
    packet = malloc(sizeof(struct iphdr) + sizeof(struct icmphdr));
    buffer = malloc(sizeof(struct iphdr) + sizeof(struct icmphdr));
    //buffer2 = malloc(sizeof(struct iphdr) + sizeof(struct tcphdr));
    /****************************************************************/
    // zero fill
	memset(packet2, 0, 4096);
	memset(buffer2, 0, 4096);

	// pointers
    ip = (struct iphdr*) packet;
    icmp = (struct icmphdr*) (packet + sizeof(struct iphdr));
    ip2 = (struct iphdr*) packet2;
	tcp = (struct tcphdr*) (packet2 + sizeof(struct iphdr));
     
    /*  
     *  here the ip packet is set up except checksum
     */
    ip->ihl          = 5;
    ip->version      = 4;
    ip->tos          = 0;
    ip->tot_len      = sizeof(struct iphdr) + sizeof(struct icmphdr);
    ip->id           = htons(random());
    ip->ttl          = 64;
    ip->protocol     = IPPROTO_ICMP;
    ip->saddr        = inet_addr(src_addr);
    ip->daddr        = inet_addr(dst_addr);
	
    if ((sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)) == -1) {
    	perror("ICMP socket failure");
	    exit(EXIT_FAILURE);
    }

	if ( (sockfd2 = socket(AF_INET, SOCK_RAW, IPPROTO_TCP)) == -1 ) {
    	perror("TCP socket failure");
	    exit(EXIT_FAILURE);

	}
     
    /* 
     *  IP_HDRINCL must be set on the socket so that
     *  the kernel does not attempt to automatically add
     *  a default ip header to the packet
     */
     
    setsockopt(sockfd, IPPROTO_IP, IP_HDRINCL, &optval, sizeof(int));
    setsockopt(sockfd2, IPPROTO_IP, IP_HDRINCL, &optval, sizeof(int));
     
    /*
     *  here the icmp packet is created
     *  also the ip checksum is generated
     */
    icmp->type           = ICMP_ECHO;
    icmp->code           = 0;
    icmp->un.echo.id     = 0;
    icmp->un.echo.sequence   = 0;
    icmp->checksum       = 0;
    icmp->checksum      = in_cksum((unsigned short *)icmp, sizeof(struct icmphdr));
     
    ip->check            = in_cksum((unsigned short *)ip, sizeof(struct iphdr));
     
    connection.sin_family = AF_INET;
    connection.sin_addr.s_addr = inet_addr(dst_addr);
    
	/*
	 * Seccond part
	 *
	 */

	// Data 
	data = packet2 + sizeof(struct iphdr) + sizeof(struct tcphdr);
	data = get_dummy_data();

    /*  
     *  here the ip2 packet is set up except checksum
     */
    ip2->ihl          = 5;
    ip2->version      = 4;
    ip2->tos          = 0;
    ip2->tot_len      = sizeof(struct iphdr) + sizeof(struct tcphdr) + strlen(data);
    ip2->id           = htons(50123);
    ip2->ttl          = 64;
    ip2->protocol     = IPPROTO_TCP;
    ip2->saddr        = inet_addr(src_addr);
    ip2->daddr        = inet_addr(dst_addr);
 
	/*
	 * tcp stuff, with full payload at SYN
	 */
    tcp->source = htons (1234);
    tcp->dest = htons (80);
    tcp->seq = 0;
    tcp->ack_seq = 0;
    tcp->doff = 5;  //tcp header size
    tcp->fin=0;
    tcp->syn=1;
    tcp->rst=0;
    tcp->psh=0;
    tcp->ack=0;
    tcp->urg=0;
    tcp->window = htons (5840); /* maximum allowed window size */
    tcp->check = 0; //leave checksum 0 now, filled later by pseudo header
    tcp->urg_ptr = 0;
    
    // Now the TCP checksum
    phdr.source_address = inet_addr( src_addr );
    phdr.dest_address = inet_addr( dst_addr );
    phdr.placeholder = 0;
    phdr.protocol = IPPROTO_TCP;
    phdr.tcp_length = htons(sizeof(struct tcphdr) + strlen(data) );
    
    int psize = sizeof(struct tcp_pseudo_hdr) + sizeof(struct tcphdr) + strlen(data);
    pseudogram = malloc(psize);
    
    memcpy(pseudogram , (char*) &phdr , sizeof (struct tcp_pseudo_hdr));
    memcpy(pseudogram + sizeof(struct tcp_pseudo_hdr) , tcp , sizeof(struct tcphdr) + strlen(data));
    
    tcp->check = in_cksum( (unsigned short*) pseudogram , psize);


	/*
     *  now the packet is sent
     */
    sendto(sockfd, packet, ip->tot_len, 0, (struct sockaddr *)&connection, sizeof(struct sockaddr));
    printf("[ICMP-ER] Sent %d byte packet to %s\n", (int) sizeof(packet), dst_addr);
     
    // now we listen for responses
    addrlen = sizeof(connection);
    if (recvfrom(sockfd, buffer, sizeof(struct iphdr) + sizeof(struct icmphdr), 0, (struct sockaddr *)&connection, &addrlen) == -1) {
	    perror("recv");
    }
    else {
	    printf("Received %d byte reply from %s:\n", (int) sizeof(buffer), dst_addr);
        ip_reply = (struct iphdr*) buffer;
	    printf("ID: %d\n", ntohs(ip_reply->id));
	    printf("TTL: %d\n", ip_reply->ttl);
    }
	
	// Packet2
	// send
	if (sendto(sockfd2, packet2, ip2->tot_len, 0, (struct sockaddr *)&connection, sizeof(struct sockaddr)) < 0) {
		perror("sendto failed");
	}
    printf("[TCP-3WH] Sent %d byte packet to %s\n", (int) ip2->tot_len, dst_addr);
     
    /*
     *  now we listen for responses
     */
    addrlen = sizeof(connection);
    //if (recvfrom(sockfd2, &buffer2, sizeof(struct iphdr) + sizeof(struct tcphdr), 0, (struct sockaddr *)&connection, &addrlen) == -1) {
    if (recvfrom(sockfd2, &buffer2, 4096, 0, (struct sockaddr *)&connection, &addrlen) == -1) {
	    perror("recv");
    }
    else {
	    printf("Received reply from %s:\n", dst_addr);
	}

    close(sockfd);
	close(sockfd2);
    return 0;
}
 
void parse_argvs(char** argv, char* dst, char* src)
{
    int i;
    if(!(*(argv + 1))) {
	    /* there are no options on the command line */
	    usage();
	    exit(EXIT_FAILURE); 
    }
    if (*(argv + 1) && (!(*(argv + 2)))) {
    /* 
     *   only one argument provided
     *   assume it is the destination server
     *   source address is local host
     */
	    strncpy(dst, *(argv + 1), 15);
    	strncpy(src, getip(), 15);
	    return;
    }
	    else if ((*(argv + 1) && (*(argv + 2)))) {
    /* 
     *    both the destination and source address are defined
     *    for now only implemented is a source address and 
     *    destination address
     */
	    strncpy(dst, *(argv + 1), 15);
	    i = 2;
	    while(*(argv + i + 1)) {
	        if (strncmp(*(argv + i), "-s", 2) == 0) {
		        strncpy(src, *(argv + i + 1), 15);
		        break;
        	}
        i++;
	    }
    }
}
 
void usage()
{
    fprintf(stderr, "\nUsage: pinger [destination] <-s [source]>\n");
    fprintf(stderr, "Destination must be provided\n");
    fprintf(stderr, "Source is optional\n\n");
}
 
char* getip()
{
    char buffer[256];
    struct hostent* h;
     
    gethostname(buffer, 256);
    h = gethostbyname(buffer);
     
    return inet_ntoa(*(struct in_addr *)h->h_addr);
     
}
/*
 * in_cksum --
 * Checksum routine for Internet Protocol
 * family headers (C Version)
 */
unsigned short in_cksum(unsigned short *addr, int len)
{
    register int sum = 0;
    u_short answer = 0;
    register u_short *w = addr;
    register int nleft = len;
    /*
     * Our algorithm is simple, using a 32 bit accumulator (sum), we add
     * sequential 16 bit words to it, and at the end, fold back all the
     * carry bits from the top 16 bits into the lower 16 bits.
     */
    while (nleft > 1)
    {
        sum += *w++;
        nleft -= 2;
    }
    /* mop up an odd byte, if necessary */
    if (nleft == 1)
    {
        *(u_char *) (&answer) = *(u_char *) w;
        sum += answer;
    }
    /* add back carry outs from top 16 bits to low 16 bits */
    sum = (sum >> 16) + (sum & 0xffff);       /* add hi 16 to low 16 */
    sum += (sum >> 16);               /* add carry */
    answer = ~sum;              /* truncate to 16 bits */
    return (answer);
}

char* get_dummy_data() {
	char* data = malloc( 1448 * sizeof(char));
	for (int i = 0; i < 1447; i++) {
		data[i] = 'A';
	}
	data[1447] = '\0';

	return data;
}
