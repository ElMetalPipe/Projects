# <center>Projet SAE24+21 - R&T Lannion</center>
# <center>Dossier technique</center>   

## Objectifs :
Objectif tester la connectivite de toutes les machines avec des vlans simples

Automatiser l'attribution d'ip en changeant le port pour acceder a un autre vlan pour montrer le fonctionnement

Pas de port multi vlans pour machine simple mais clone a fonction differente pour celle-ci


## Attribution des ports/vlans :

2-4 :2  
5-7 :3  
8-10 :5  
11-13 :6  
14-16 :7  
17-19 :8  
20-21 :9  
22 :4  
23 :interswitchs  
24 :interswitchs/interrouteur


## Switch Cisco (étage) :

```
en
conf t
vlan 2
exit
vlan 3
exit
vlan 4
exit
vlan 5
exit
vlan 6
exit
vlan 7
exit
vlan 8
exit
vlan 9
exit
int range fa0/2 - 4
switchport mode access
switchport access vlan 2
exit
int range fa0/5 - 7
switchport mode access
switchport access vlan 3
exit
int range fa0/8 - 10
switchport mode access
switchport access vlan 5
exit
int range fa0/11 - 13
switchport mode access
switchport access vlan 6
exit
int range fa0/14 - 16
switchport mode access
switchport access vlan 7
exit
int range fa0/17 - 19
switchport mode access
switchport access vlan 8
exit
int range fa0/20 - 21
switchport mode access
switchport access vlan 9
exit
int fa0/22
switchport mode access
switchport access vlan 4
exit
int fa0/23
switchport mode trunk
switchport trunk allowed vlan 2,3,4,5,6,7,8,9
exit
int fa0/24
switchport mode trunk
switchport trunk allowed vlan 2,3,4,5,6,7,8,9
exit
hostname S-etage-cisco1
```

*Pour reset config :*
- delete flash:vlan.dat
- erase startup-config
- reload (valider sans sauvegarder)



## Switch Aruba (RDC & étage) :

```
conf t
vlan 2
name "VLAN2"  
untagged 2-4
tagged 23-24
no ip address
exit
vlan 3
name "VLAN3"
untagged 5-7
tagged 23-24
no ip address
exit
vlan 4
name "VLAN4"
untagged 22
tagged 23-24
no ip address
exit
vlan 5
name "VLAN5"
untagged 8-10
tagged 23-24
no ip address
exit
vlan 6
name "VLAN6"
untagged 11-13
tagged 23-24
no ip address
exit
vlan 7
name "VLAN7"
untagged 14-16
tagged 23-24
no ip address
exit
vlan 8
name "VLAN8"
untagged 17-19
tagged 23-24
no ip address
exit
vlan 9
name "VLAN9"
untagged 20-21
tagged 23-24
no ip address
exit
hostname S-etage-aruba1
```

*Pour reset config :*
- erase startup-config
- reload

## Routeur Cisco (RDC) :

```
conf t
interface FastEthernet0/0
ip address 175.45.176.251 255.255.255.0
no shut
exit
interface FastEthernet0/0/0
no shut
exit
interface FastEthernet0/0/0.2
encapsulation dot1Q 2
ip address 10.0.1.70 255.255.255.248
ip helper-address 192.168.240.2
exit
interface FastEthernet0/0/0.3
encapsulation dot1Q 3
ip address 10.0.0.254 255.255.255.0
ip helper-address 192.168.240.2
exit
interface FastEthernet0/0/0.4
encapsulation dot1Q 4
ip address 192.168.240.254 255.255.255.0
exit
interface FastEthernet0/0/0.5
 encapsulation dot1Q 5
ip address 10.0.4.254 255.255.255.0
ip helper-address 192.168.240.2 
exit
interface FastEthernet0/0/0.6
encapsulation dot1Q 6
ip address 10.0.3.254 255.255.254.0
ip helper-address 192.168.240.2 
exit
interface FastEthernet0/0/0.7
encapsulation dot1Q 7
ip address 10.0.6.254 255.255.255.0
ip helper-address 192.168.240.2 
exit
interface FastEthernet0/0/0.8
encapsulation dot1Q 8
ip address 10.0.5.254 255.255.255.0
ip helper-address 192.168.240.2 
exit
interface FastEthernet0/0/0.9
encapsulation dot1Q 9
ip address 10.0.1.62 255.255.255.192
ip helper-address 192.168.240.2  
exit
ip route 0.0.0.0 0.0.0.0 175.45.176.254
ip routing
hostname r-main
```

*Pour reset config :*
- copy flash:vierge2811.cfg startup-config
- reload

## Serveur DHCP :

### Client :

- Activer service DHCP : dhclient -v eth0
- Désactiver service DHCP : dhclient -r eth0 (a faire pour vider le lease et changer de vlan)


### Serveur :

- Mettre une @ip + route par défaut
- Configurer le fichier /etc/dhcpd.conf
- Activer le service dchp (systemctl start isc-dhcp-server)
- Activer trames dhcp sur toutes les sous interfaces du routeur
- Penser à brancher au mur + baie de brassage

### /etc/dhcpd.conf :

```
ddns-update-style none;

default-lease-time 600;
max-lease-time 600;

subnet 192.168.240.0 netmask 255.255.255.0 {
  range 192.168.240.11 192.168.240.20;
  option routers 192.168.240.254;
  option broadcast-address 192.168.240.255;
  host serv-main {
    hardware ethernet 2c:58:b9:10:26:6c;
    fixed-address 192.168.240.2; }
  host serv-etage {
    hardware ethernet 2c:58:b9:10:2b:1e;
    fixed-address 192.168.240.6;  }
}
subnet 10.0.0.0 netmask 255.255.255.0 {
  range 10.0.0.1 10.0.0.253;
  option routers 10.0.0.254;
  option broadcast-address 10.0.0.255;
}
subnet 10.0.1.0 netmask 255.255.255.192 {
  range 10.0.1.1 10.0.1.61;
  option routers 10.0.1.62;
  option broadcast-address 10.0.1.63;
}
subnet 10.0.1.64 netmask 255.255.255.248 {
  range 10.0.1.65 10.0.1.69;
  option routers 10.0.1.70;
  option broadcast-address 10.0.1.71;
}
subnet 10.0.2.0 netmask 255.255.254.0 {
  range 10.0.2.1 10.0.3.253;
  option routers 10.0.3.254;
  option broadcast-address 10.0.3.255;
}
subnet 10.0.4.0 netmask 255.255.255.0 {
  range 10.0.4.1 10.0.4.253;
  option routers 10.0.4.254;
  option broadcast-address 10.0.4.255;
}
subnet 10.0.5.0 netmask 255.255.255.0 {
  range 10.0.5.1 10.0.5.253;
  option routers 10.0.5.254;
  option broadcast-address 10.0.5.255;
}
subnet 10.0.6.0 netmask 255.255.255.0 {
  range 10.0.6.1 10.0.6.253;
  option routers 10.0.6.254;
  option broadcast-address 10.0.6.255;
}
```

> Les adresses fixes du DHCP ne correspondent pas aux adresses du Schema de depannage 
> Ainsi il y aura aussi une erreur dans la conf du routeur avec les trames dhcp (ip-helper) /\
> Changement a faire dans le dhcp : ajout du serveur dns
> Ajouter une adresse ip fixe pour la directrice/patron

```
#  option domain-name-servers ns1.internal.example.org;
#  option domain-name "internal.example.org";
```

## DNS 

- Ordre de résolution de noms : /etc/nsswitch.conf
- Résolution locale : /etc/hosts
- Résolution de noms : /etc/resolv.conf
- Nom du service : named
- Fichier de configuration principal du serveur : /etc/bind/named.conf
- Zones par défaut : /etc/bind/named.conf.default-zones
- Listes des zones gérées par le serveur : /etc/bind/named.conf.local
- Configuration des options : /etc/bind/named.conf.options

### DNS_1 (192.168.240.1/24) :

#### Config de /etc/nsswitch :


#### Config de /etc/hosts :


#### Config de /etc/resolv.conf :


### DNS_2 (192.168.240.6/24) :

#### Côté client :

##### Config de /etc/nsswitch :
```
hosts : files mdns4_minimal [NOTFOUND=return] dns
```

##### Config de /etc/hosts :
```
127.0.0.1             	 	 localhost
10.254.4.1              s4
10.4.1.1                s4
10.4.1.1                s4.tp41.iut
10.4.2.1                s4
10.4.2.1                s4.tp42.iut
192.168.240.1           serv-dns1
192.168.240.2           serv-dhcp
192.168.240.3           serv-partage
192.168.240.4           serv-web
192.168.240.5           serv-controleur
192.168.240.6           serv-dns2
```
*Non nécessaire*

##### Config de /etc/resolv.conf :
```
search svart-hotel.no no
nameserver 192.168.240.1 10.254.0.254
```
#### Côté serveur :
/
##### Config de /bind/named.conf :
/
##### Config de /bind/named.conf.default-zones :
```
zone "." {
	type hint;
	file "/usr/share/dns/root.hints";
};

// be authoritative for the localhost forward and reverse zones, and for
// broadcast zones as per RFC 1912

zone "localhost" {
	type master;
	file "/etc/bind/db.local";
};

zone "127.in-addr.arpa" {
	type master;
	file "/etc/bind/db.127";
};

zone "0.in-addr.arpa" {
	type master;
	file "/etc/bind/db.0";
};

zone "255.in-addr.arpa" {
	type master;
	file "/etc/bind/db.255";
};

zone "svart-hotel.no" {
	type master;
	file "/etc/bind/db.svart-hotel.no";
};

zone "240.168.192.in-addr.arpa" {
	type master;
	file "/etc/bind/db.192.168.240";
};

```
##### Config de /bind/named.conf.local :
/
##### Config de /bind/named.conf.options :
- Forwarder a mettre
##### Config de /bind/db.svart-hotel.no :
```
$ORIGIN svart-hotel.no.
$TTL	604800
@	IN	SOA	dns2.svart-hotel.no. root.svart-hotel.no. (
			      1		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	dns2.svart-hotel.no.
dns1    IN  A 192.168.240.1
dhcp    IN  A 192.168.240.2
partage IN  A 192.168.240.3
web     IN  A 192.168.240.4
controleur    IN  A 192.168.240.5
dns2    IN  A 192.168.240.6
```

> Ajout de nom a faire + groupe (peut etre)
> Faire inverse aussi

##### Config de /bind/db.192.168.240 :
```
$ORIGIN 240.168.192.in-addr.arpa.
$TTL	604800
@	IN	SOA	dns2.svart-hotel.no. root.svart-hotel.no. (
			      1		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	dns2.svart-hotel.no.
1    IN  PTR dns1
2    IN  PTR dhcp
3    IN  PTR partage
4    IN  PTR web
5    IN  PTR controleur
6    IN  PTR dns2
```

## NAT :

### Config pour le routeur RDC : 
```
access-list 1 permit 10.0.1.64 0.0.0.7
access-list 1 permit 10.0.0.0 0.0.0.255
access-list 1 permit 192.168.240.0 0.0.0.255
access-list 1 permit 10.0.4.0 0.0.0.255
access-list 1 permit 10.0.2.0 0.0.1.255
access-list 1 permit 10.0.6.0 0.0.0.255
access-list 1 permit 10.0.5.0 0.0.0.255
access-list 1 permit 10.0.1.0 0.0.0.127
ip nat inside source list 1 interface FastEthernet0/0 overload
interface FastEthernet0/0/0.2
ip nat inside
exit
interface FastEthernet0/0/0.3
ip nat inside
exit
interface FastEthernet0/0/0.4
ip nat inside
exit
interface FastEthernet0/0/0.5
ip nat inside
exit
interface FastEthernet0/0/0.6
ip nat inside
exit
interface FastEthernet0/0/0.7
ip nat inside
exit
interface FastEthernet0/0/0.8
ip nat inside
exit
interface FastEthernet0/0/0.9
ip nat inside
exit
interface FastEthernet0/0
ip nat outside
```

> Erreur possible à la première ligne.

## Active Directory :

> Ajouter schema

### Utilisateurs :

### Groupes :

### Droits

### Partage?






#### Preuve de fonctionnement du reseau

### 5. Serveur apache

### 6. AD



### Autres :

- DNS2

- Client Windows

- Client Linux

- WEB

chopper cours de droits + ad

rapport a autant de poids que le rapport