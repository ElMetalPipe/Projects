# <center>Projet SAE24+21 - R&T Lannion</center>
# <center>Dossier technique</center>

<center>Par Delafosse Quentin & Renault Louison
<br>

*Dossier entièrement rédigé par Quentin, les contributions seront affichées près des titres dans la forme suivante : %Quentin/%Louison*  
*Exemple : DNS [50/50]*

</center>

## Objectifs :
Ce dossier présente toutes les informations nécessaires et complémentaire à la mise en place du réseau pour l'Hotel Svart.  
Des liens cliquables sont présents pour vous rediriger vers le fichier de configuration en question.

## Rappel des services demandés :

- Différents VLAN pour les groupes qui composent le réseau
- Service DHCP pour auto-attribution des @ips
- Services DNS pour résolution de noms
- NAT pour accéder et sécuriser l'accès vers l'extérieur
- Service WEB pour le site de l'hotel
- Active Directory pour partage de fichiers, droits et second DNS

## <center>Sommaire</center>
<center>
  
[Scripts de configuration matérielle](#script-conf)  
[Configurations courantes du matériel](#run-conf)  
[DHCP](#DHCP)  
[DNS](#DNS)   
[NAT](#NAT)  
[WEB](#WEB)  
[AD](#AD)  
[Preuves](#Preuves)

</center>


## Scripts de configuration matérielles<a id="script-conf"></a>
> Scripts à éxécuter dans l'ordre suivant

### Switch Aruba (RDC & étage) : [50/50]
[Lien vers le fichier de S-main-aruba](C2_1_RdV4_Ressources_Delafosse-Renault/config/config%20de%20s-main-aruba)    
[Lien vers le fichier de S-etage-aruba1](C2_1_RdV4_Ressources_Delafosse-Renault/config/config%20de%20s-etage-aruba1)
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
exit
write memory
```
*Pour le RDC : hostname S-main-aruba*  
*Ici 'write memory' permet de sauvegarder la configuration afin que l'équipement soit opérationnel dès le démarrage.*

*Pour reset config :*
- erase startup-config
- reload

### Routeur Cisco (RDC) : [0/100]
[Lien vers le fichier](C2_1_RdV4_Ressources_Delafosse-Renault/config/config%20de%20r-main-cisco)
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
hostname R-main
exit
copy running-config startup-config   
```
*Ici 'copy running-config startup-config' permet de sauvegarder la configuration afin que l'équipement soit opérationnel dès le démarrage.*

*Pour reset config :*
- copy flash:vierge2811.cfg startup-config
- reload

### Switch Cisco (étage) : [100/0]
[Lien vers le fichier](C2_1_RdV4_Ressources_Delafosse-Renault/config/config%20de%20s-etage-cisco1)
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
exit
copy running-config startup-config
```
*Ici 'copy running-config startup-config' permet de sauvegarder la configuration afin que l'équipement soit opérationnel dès le démarrage.*

*Pour reset config :*
- delete flash:vlan.dat
- erase startup-config
- reload (valider sans sauvegarder)

## Configuration courante du matériel<a id="run-conf"></a>

### Switch Aruba (RDC & étage) :

> Les configurations des 2 switchs sont les mêmes. Seul le nom diffère.

[Lien vers le fichier de S-etage-aruba1](C2_1_RdV4_Ressources_Delafosse-Renault/run/run%20s-etage-aruba1)


```
S-etage-aruba1(config)# sh run                                                  
                                                                                
Running configuration:                                                          
                                                                                
; JL261A Configuration Editor; Created on release #WC.16.07.0003                
; Ver #14:01.4f.f8.1d.9b.3f.bf.bb.ef.7c.59.fc.6b.fb.9f.fc.ff.ff.37.ef:02        
hostname "S-etage-aruba1"                                                       
module 1 type jl261a                                                            
snmp-server community "public" unrestricted                                     
vlan 1                                                                          
   name "DEFAULT_VLAN"                                                          
   no untagged 2-22                                                             
   untagged 1,23-28                                                             
   ip address dhcp-bootp                                                        
   ipv6 enable                                                                  
   ipv6 address dhcp full                                                       
   exit                                                                         
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

```

### Routeur Cisco (RDC) :

[Lien vers le fichier de R-main-cisco](C2_1_RdV4_Ressources_Delafosse-Renault/run/run%20r-main-cisco)

```
r-main-cisco(config-if)#do sh run                                               
Building configuration...                                                       
                                                                                
                                                                                
Current configuration : 3181 bytes                                              
!                                                                               
version 15.1                                                                    
service timestamps debug datetime msec                                          
service timestamps log datetime msec                                            
no service password-encryption                                                  
!                                                                               
hostname r-main-cisco                                                           
!                                                                               
boot-start-marker                                                               
boot system flash c2800nm-adventerprisek9-mz.151-3.T.bin                        
boot-end-marker                                                                 
!                                                                               
!                                                                               
enable password lannion                                                         
!                                                                               
no aaa new-model                                                                
!                                                                               
memory-size iomem 5                                                             
!                                                                               
dot11 syslog                                                                    
ip source-route                                                                 
!                                                                               
!                                                                               
ip cef                                                                          
!                                                                               
!                                                                               
!                                                                               
no ip domain lookup                                                             
no ipv6 cef                                                                     
!                                                                               
multilink bundle-name authenticated                                             
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
voice-card 0                                                                    
!                                                                               
crypto pki token default removal timeout 0                                      
!                                                                               
!                                                                               
!                                                                               
!                                                                               
license udi pid CISCO2811 sn FCZ12157163                                        
archive                                                                         
 log config                                                                     
  hidekeys                                                                      
!                                                                               
redundancy                                                                      
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
interface FastEthernet0/0                                                       
 ip address 175.45.176.251 255.255.255.0                                        
 no ip proxy-arp                                                                
 ip nat outside                                                                 
 ip virtual-reassembly in                                                       
 duplex auto                                                                    
 speed auto                                                                     
!                                                                               
interface FastEthernet0/1                                                       
 no ip address                                                                  
 no ip proxy-arp                                                                
 shutdown                                                                       
 duplex auto                                                                    
 speed auto                                                                     
!                                                                               
interface FastEthernet0/0/0                                                     
 no ip address                                                                  
 no ip proxy-arp                                                                
 duplex auto                                                                    
 speed auto                                                                     
!                                                                               
interface FastEthernet0/0/0.2                                                   
 encapsulation dot1Q 2                                                          
 ip address 10.0.1.70 255.255.255.248                                           
 ip helper-address 192.168.240.2                                                
 ip nat inside                                                                  
 ip virtual-reassembly in                                                       
 no cdp enable                                                                  
!                                                                               
interface FastEthernet0/0/0.3                                                   
 encapsulation dot1Q 3                                                          
 ip address 10.0.0.254 255.255.255.0                                            
 ip helper-address 192.168.240.2                                                
 ip nat inside                                                                  
 ip virtual-reassembly in                                                       
 no cdp enable                                                                  
!                                                                               
interface FastEthernet0/0/0.4                                                   
 encapsulation dot1Q 4                                                          
 ip address 192.168.240.254 255.255.255.0                                       
 ip nat inside                                                                  
 ip virtual-reassembly in                                                       
 no cdp enable                                                                  
!                                                                               
interface FastEthernet0/0/0.5                                                   
 encapsulation dot1Q 5                                                          
 ip address 10.0.4.254 255.255.255.0                                            
 ip helper-address 192.168.240.2                                                
 ip nat inside                                                                  
 ip virtual-reassembly in                                                       
 no cdp enable                                                                  
!                                                                               
interface FastEthernet0/0/0.6                                                   
 encapsulation dot1Q 6                                                          
 ip address 10.0.3.254 255.255.254.0                                            
 ip helper-address 192.168.240.2                                                
 ip nat inside                                                                  
 ip virtual-reassembly in                                                       
 no cdp enable                                                                  
!                                                                               
interface FastEthernet0/0/0.7                                                   
 encapsulation dot1Q 7                                                          
 ip address 10.0.6.254 255.255.255.0                                            
 ip helper-address 192.168.240.2                                                
 ip nat inside                                                                  
 ip virtual-reassembly in                                                       
 no cdp enable                                                                  
!                                                                               
interface FastEthernet0/0/0.8                                                   
 encapsulation dot1Q 8                                                          
 ip address 10.0.5.254 255.255.255.0                                            
 ip helper-address 192.168.240.2                                                
 ip nat inside                                                                  
 ip virtual-reassembly in                                                       
 no cdp enable                                                                  
!                                                                               
interface FastEthernet0/0/0.9                                                   
 encapsulation dot1Q 9                                                          
 ip address 10.0.1.62 255.255.255.192                                           
 ip helper-address 192.168.240.2                                                
 ip nat inside                                                                  
 ip virtual-reassembly in                                                       
 no cdp enable                                                                  
!                                                                               
interface Serial0/3/0                                                           
 no ip address                                                                  
 shutdown                                                                       
 clock rate 2000000                                                             
!                                                                               
ip forward-protocol nd                                                          
no ip http server                                                               
no ip http secure-server                                                        
!                                                                               
!                                                                               
ip nat inside source list 1 interface FastEthernet0/0 overload                  
ip route 0.0.0.0 0.0.0.0 175.45.176.254                                         
!                                                                               
logging esm config                                                              
access-list 1 permit 10.0.1.64 0.0.0.7                                          
access-list 1 permit 10.0.0.0 0.0.0.255                                         
access-list 1 permit 192.168.240.0 0.0.0.255                                    
access-list 1 permit 10.0.4.0 0.0.0.255                                         
access-list 1 permit 10.0.2.0 0.0.1.255                                         
access-list 1 permit 10.0.6.0 0.0.0.255                                         
access-list 1 permit 10.0.5.0 0.0.0.255                                         
access-list 1 permit 10.0.1.0 0.0.0.127                                         
no cdp run                                                                      
                                                                                
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
control-plane                                                                   
!                                                                               
!                                                                               
!                                                                               
mgcp fax t38 ecm                                                                
!                                                                               
mgcp profile default                                                            
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
!                                                                               
line con 0                                                                      
 logging synchronous                                                            
line aux 0                                                                      
line vty 0 4                                                                    
 login                                                                          
 transport input all                                                            
!                                                                               
scheduler allocate 20000 1000                                                   
end 

```

### Switch Cisco (étage) :

[Lien vers le fichier de S-etage-cisco1](C2_1_RdV4_Ressources_Delafosse-Renault/run/run%20s-etage-cisco1)

```
S-etage-cisco1(config)#do sh run                                                
Building configuration...                                                       
                                                                                
Current configuration : 2311 bytes                                              
!                                                                               
version 12.1                                                                    
no service pad                                                                  
service timestamps debug uptime                                                 
service timestamps log uptime                                                   
no service password-encryption                                                  
!                                                                               
hostname S-etage-cisco1                                                         
!                                                                               
!                                                                               
ip subnet-zero                                                                  
!                                                                               
ip ssh time-out 120                                                             
ip ssh authentication-retries 3                                                 
!                                                                               
spanning-tree mode pvst                                                         
no spanning-tree optimize bpdu transmission                                     
spanning-tree extend system-id                                                  
!                                                                               
!                                                                               
!                                                                               
                                                                                
S-etage-cisco1(config)#do sh run                                                
Building configuration...                                                       
                                                                                
Current configuration : 2311 bytes                                              
!                                                                               
version 12.1                                                                    
no service pad                                                                  
service timestamps debug uptime                                                 
service timestamps log uptime                                                   
no service password-encryption                                                  
!                                                                               
hostname S-etage-cisco1                                                         
!                                                                               
!                                                                               
ip subnet-zero                                                                  
!                                                                               
ip ssh time-out 120                                                             
ip ssh authentication-retries 3                                                 
!                                                                               
spanning-tree mode pvst                                                         
no spanning-tree optimize bpdu transmission                                     
spanning-tree extend system-id                                                  
!                                                                               
!                                                                               
!                                                                               
!                                                                               
interface FastEthernet0/1                                                       
!                                                                               
interface FastEthernet0/2                                                       
 switchport access vlan 2                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/3                                                       
 switchport access vlan 2                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/4                                                       
 switchport access vlan 2                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/5                                                       
 switchport access vlan 3                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/6                                                       
 switchport access vlan 3                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/7                                                       
 switchport access vlan 3                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/8                                                       
 switchport access vlan 5                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/9                                                       
 switchport access vlan 5                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/10                                                      
 switchport access vlan 5                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/11                                                      
 switchport access vlan 6                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/12                                                      
 switchport access vlan 6                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/13                                                      
 switchport access vlan 6                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/14                                                      
 switchport access vlan 7                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/15                                                      
 switchport access vlan 7                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/16                                                      
 switchport access vlan 7                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/17                                                      
 switchport access vlan 8                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/18                                                      
 switchport access vlan 8                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/19                                                      
 switchport access vlan 8                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/20                                                      
 switchport access vlan 9                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/21                                                      
 switchport access vlan 9                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/22                                                      
 switchport access vlan 4                                                       
 switchport mode access                                                         
!                                                                               
interface FastEthernet0/23                                                      
 switchport trunk allowed vlan 2-9                                              
 switchport mode trunk                                                          
!                                                                               
interface FastEthernet0/24                                                      
 switchport trunk allowed vlan 2-9                                              
 switchport mode trunk                                                          
!                                                                               
interface Vlan1                                                                 
 ip address 10.254.200.109 255.255.0.0                                          
 no ip route-cache                                                              
!                                                                               
ip http server                                                                  
!                                                                               
line con 0                                                                      
line vty 5 15                                                                   
!                                                                               
!                                                                               
end                                                                             

```

## Serveur DHCP [35/65]<a id="DHCP"></a> :

Le service permet d'attribuer de manière automatique une adresse ipv4, son masque et une route par défaut aux clients. En parallèle de cela des informations sur le serveur dns à contacter et les nom de domaines à utiliser sont aussi envoyées.

### Client :
#### Au démarrage :
- Les machines sont cliente DHCP au démarrage via une modification du fichier /etc/network/interfaces
```
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet dhcp
```

#### Pour changer le VLAN des machines :
- Il faut redémarrer le service réseau : systemctl restart networking

#### En mode debug :
- Activer service DHCP : dhclient -v eth0
- Désactiver service DHCP : dhclient -r eth0 (à faire pour vider le lease et changer de vlan si non automatique)


### Serveur :

- Mettre une @ip + route par défaut statique dans /etc/network/interfaces
```
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 192.168.240.2
    netmask 255.255.255.0
    gateway 192.168.240.254
```
- Redémarrer le service réseau : systemctl restart networking
- Configurer le fichier /etc/dhcpd.conf
- Activer le service dchp (systemctl start isc-dhcp-server)
- Activer trames dhcp sur toutes les sous interfaces du routeur
- Penser à brancher au mur + baie de brassage

### /etc/dhcpd.conf :
[Lien vers le fichier dhcpd.conf](C2_1_RdV4_Ressources_Delafosse-Renault/dhcp/dhcpd.conf)
```
ddns-update-style none;

default-lease-time 600;
max-lease-time 600;
option domain-name-servers 192.168.240.2;
option domain-search "hs25.iut", "iut";

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
  host pc-directeur {
   hardware ethernet F4:8E:38:84:69:F8;
   fixed-address 10.0.1.1;  }
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
> Pour activer le serveur DHCP au démarrage il faut effectuer la commande suivante :
> ```
> systemctl enable isc-dhcp-server
> ```
> <br>

## DNS [65/35]<a id="DNS"></a> :

#### Notions importantes :

- Ordre de résolution de noms : /etc/nsswitch.conf
- Résolution locale : /etc/hosts
- Résolution de noms : /etc/resolv.conf
- Nom du service : named
- Fichier de configuration principal du serveur : /etc/bind/named.conf
- Zones par défaut : /etc/bind/named.conf.default-zones
- Listes des zones gérées par le serveur : /etc/bind/named.conf.local
- Configuration des options : /etc/bind/named.conf.options

### DNS_1 (192.168.240.2/24) :

#### Côté client :

##### Config de /etc/nsswitch :
[Lien vers le fichier nsswitch](C2_1_RdV4_Ressources_Delafosse-Renault/dns/nsswitch.conf)
```
hosts : files mdns4_minimal [NOTFOUND=return] dns
```

##### Config de /etc/hosts :
[Lien vers le fichier hosts](C2_1_RdV4_Ressources_Delafosse-Renault/dns/hosts)
```
127.0.0.1             	 	 localhost
192.168.240.2           dns1
192.168.240.2           dhcp
192.168.240.6           partage
192.168.240.2           intra
192.168.240.6           controleur
192.168.240.6           dns2
```
*Exemple de remplissage du fichier hosts, non indispensable*

##### Config de /etc/resolv.conf :
[Lien vers le fichier resolv.conf](C2_1_RdV4_Ressources_Delafosse-Renault/dns/resolv.conf)
```
search hs25.iut iut
nameserver 192.168.240.2
```
*Ce fichier se remplit de manière automatique via le serveur DHCP*
#### Côté serveur :

##### Config de /bind/named.conf.default-zones :
[Lien vers le fichier named.conf.default-zones](C2_1_RdV4_Ressources_Delafosse-Renault/dns/bind/named.conf.default-zones)
```
// prime the server with knowledge of the root servers
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

zone "hs25.iut" {
	type master;
	file "/etc/bind/db.hs25.iut";
};

zone "240.168.192.in-addr.arpa" {
	type master;
	file "/etc/bind/db.192.168.240";
};
zone "64.1.0.10.in-addr.arpa" {
	type master;
	file "/etc/bind/db.10.0.1.64";
};
zone "4.0.10.in-addr.arpa" {
	type master;
	file "/etc/bind/db.10.0.4";
};
zone "5.0.10.in-addr.arpa" {
	type master;
	file "/etc/bind/db.10.0.5";
};
zone "2.0.10.in-addr.arpa" {
	type master;
	file "/etc/bind/db.10.0.2";
};
zone "6.0.10.in-addr.arpa" {
	type master;
	file "/etc/bind/db.10.0.6";
};

```

##### Config de /bind/db.hs25.iut :
[Lien vers le fichier db.hs25.iut](C2_1_RdV4_Ressources_Delafosse-Renault/dns/bind/db.hs25.iut)
```
$ORIGIN hs25.iut.
$TTL	604800
@	IN	SOA	dns1.hs25.iut. root.hs25.iut. (
			      1		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	dns1.hs25.iut.
dns1    IN  A 192.168.240.2
dhcp    IN  A 192.168.240.2
partage IN  A 192.168.240.6
intra     IN  A 192.168.240.2
controleur    IN  A 192.168.240.6
dns2    IN  A 192.168.240.6
imprimante1    IN  A 10.0.1.65
domotique1    IN  A 10.0.4.1
television1    IN  A 10.0.5.1
client1    IN  A 10.0.2.1
telephone1    IN  A 10.0.6.1
telephone2    IN  A 10.0.6.2
```

##### Config de /bind/db.192.168.240 :
[Lien vers le fichier db.192.168.240](C2_1_RdV4_Ressources_Delafosse-Renault/dns/bind/db.192.168.240)
```
$ORIGIN 240.168.192.in-addr.arpa.
$TTL	604800
@	IN	SOA	dns2.hs25.iut. root.hs25.iut. (
			      1		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	dns1.hs25.iut.
2    IN  PTR dns1
2    IN  PTR dhcp
6    IN  PTR partage
2    IN  PTR intra
6    IN  PTR controleur
6    IN  PTR dns2
```

##### Config de /bind/db.10.0.1.64 :
[Lien vers le fichier db.10.0.1.64](C2_1_RdV4_Ressources_Delafosse-Renault/dns/bind/db.10.0.1.64)
```
$ORIGIN 64.1.0.10.in-addr.arpa.
$TTL	604800
@	IN	SOA	dns1.hs25.iut. root.hs25.iut. (
			      1		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	dns1.hs25.iut.
65    IN  PTR imprimante1
```

##### Config de /bind/db.10.0.2 :
[Lien vers le fichier db.10.0.2](C2_1_RdV4_Ressources_Delafosse-Renault/dns/bind/db.10.0.2)
```
$ORIGIN 2.0.10.in-addr.arpa.
$TTL	604800
@	IN	SOA	dns1.hs25.iut. root.hs25.iut. (
			      1		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	dns1.hs25.iut.
1    IN  PTR client1
```

##### Config de /bind/db.10.0.4 :
[Lien vers le fichier db.10.0.4](C2_1_RdV4_Ressources_Delafosse-Renault/dns/bind/db.10.0.4)
```
$ORIGIN 4.0.10.in-addr.arpa.
$TTL	604800
@	IN	SOA	dns1.hs25.iut. root.hs25.iut. (
			      1		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	dns1.hs25.iut.
1    IN  PTR domotique1
```

##### Config de /bind/db.10.0.5 :
[Lien vers le fichier db.10.0.5](C2_1_RdV4_Ressources_Delafosse-Renault/dns/bind/db.10.0.5)
```
$ORIGIN 5.0.10.in-addr.arpa.
$TTL	604800
@	IN	SOA	dns1.hs25.iut. root.hs25.iut. (
			      1		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	dns1.hs25.iut.
1    IN  PTR television1
```

##### Config de /bind/db.10.0.6 :
[Lien vers le fichier db.10.0.6](C2_1_RdV4_Ressources_Delafosse-Renault/dns/bind/db.10.0.6)
```
$ORIGIN 6.0.10.in-addr.arpa.
$TTL	604800
@	IN	SOA	dns1.hs25.iut. root.hs25.iut. (
			      1		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	dns1.hs25.iut.
1    IN  PTR telephone1
2    IN  PTR telephone2
```

> Pour activer le serveur DNS au démarrage il faut effectuer la commande suivante :
> ```
> systemctl enable named
> ```
> <br>

#### Pour tester le service DNS :

- dig [nom_de_domaine] 
- Exemple : dig dhcp

## NAT [0/100]<a id="NAT"></a> :

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

> Cette partie est déjà intégrée au script du routeur cisco

## Apache [0/100]<a id="WEB"></a> :

### Serveur :

- Effectuer la commande : htpasswd -c /etc/apache2/.htpasswd Identifiant
- Entrer un mdp puis le confirmer
- Activer le service apache : systemctl start apache2

*Format URL : http://user:pass@www.iut-lannion.fr:8080/index.html*

### Config pour le serveur apache :

#### /var/www/hs25.iut/intra/.htaccess :
[Lien vers le fichier .htaccess](C2_1_RdV4_Ressources_Delafosse-Renault/apache/var/www/hs25.iut/intra/.htaccess)
```
AuthType Basic
AuthName "Zone privée"
AuthUserFile /etc/apache2/.htpasswd
Require valid-user
```


#### /etc/apache2/apache2.conf :
[Lien vers le fichier apache2.conf](C2_1_RdV4_Ressources_Delafosse-Renault/apache/etc/apache2/apache2.conf)
```
ServerName hs25.iut

DefaultRuntimeDir ${APACHE_RUN_DIR}

PidFile ${APACHE_PID_FILE}

Timeout 300

KeepAlive On

MaxKeepAliveRequests 100

KeepAliveTimeout 5

User ${APACHE_RUN_USER}
Group ${APACHE_RUN_GROUP}

HostnameLookups Off

ErrorLog ${APACHE_LOG_DIR}/error.log

LogLevel warn

IncludeOptional mods-enabled/*.load
IncludeOptional mods-enabled/*.conf

Include ports.conf

<Directory />
	Options FollowSymLinks
	AllowOverride None
	Require all denied
</Directory>

<Directory /usr/share>
	AllowOverride None
	Require all granted
</Directory>

<Directory /var/www/>
	Options Indexes FollowSymLinks
	AllowOverride None
	Require all granted
</Directory>
</Directory>

AccessFileName .htaccess

<FilesMatch "^\.ht">
	Require all denied
</FilesMatch>


LogFormat "%v:%p %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" vhost_combined
LogFormat "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" combined
LogFormat "%h %l %u %t \"%r\" %>s %O" common
LogFormat "%{Referer}i -> %U" referer
LogFormat "%{User-agent}i" agent

IncludeOptional conf-enabled/*.conf

IncludeOptional sites-enabled/*.conf

```

#### /etc/apache2/sites-available/000-default.conf :
[Lien vers le fichier 000-default.conf](C2_1_RdV4_Ressources_Delafosse-Renault/apache/etc/apache2/sites-available/000-default.conf)
```
<VirtualHost *:80>
	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/hs25.iut

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
	
	<Directory /var/www/hs25.iut>
		Options Indexes FollowSymLinks
		AllowOverride None
		Require all granted
		DirectoryIndex index.html		
	</Directory>
	
	<Directory /var/www/hs25.iut/wan>
		Options Indexes FollowSymLinks
		AllowOverride All
		Require all granted
		DirectoryIndex index.html		
	</Directory>
	
	<Directory /var/www/hs25.iut/intra>
		Options Indexes FollowSymLinks
		AllowOverride None
		Require all granted
		DirectoryIndex index.html
		Require ip 10.0.0.0/24 10.0.1.0/26 10.0.1.64/29 10.0.2.0/23 10.0.4.0/24 10.0.5.0/24 10.0.6.0/24 192.168.240.0/24 
	</Directory>

</VirtualHost>
```

> Pour activer le serveur apache au démarrage il faut effectuer la commande suivante :
> ```
> systemctl enable apache2
> ```
> <br>

## Active Directory [100/0]<a id="AD"></a> :

### Utilisateurs :
![alt text](Preuves/Preuve_AD5.png)
### Répertoires personnels :
![alt text](Preuves/Preuve_AD12.png)
### Groupes de sécurité :
![alt text](Preuves/Preuve_AD6.png)
### Partage :
![alt text](Preuves/Preuve_AD7.png)
![alt text](Preuves/Preuve_AD8.png)
![alt text](Preuves/Preuve_AD9.png)

### Schéma des Groupes & Utilisateurs :
![alt text](Preuves/Preuve_AD10.png)
### Schéma de Sécurité & Partage :
![alt text](Preuves/Preuve_AD11.png)

### DNS_2 (192.168.240.6/24)
##### Zone de recherche directe :
![alt text](Preuves/Preuve_AD2.png)
##### Exemple de Recherche inversée pour le réseau de la Direction :
![alt text](Preuves/Preuve_AD3.png)
##### Exemple de Recherche inversée pour le réseau des serveurs :
![alt text](Preuves/Preuve_AD4.png)

## Preuves de fonctionnement du réseau<a id="Preuves"></a> :

### 1. VLAN + Routage [50/50]

![alt text](Preuves/preuve_VLAN+routage_G4.png)
> Ping de G4 Linux (10.0.1.65) appartenant au VLAN imprimantes [2] vers D4 Linux (10.0.0.2) appartenant au VLAN employés [3]

![alt text](Preuves/preuve_vlan+routage_D05.png)
> Ping de D5 Windows (10.0.1.1) appartenant au VLAN Direction [1] vers G5 Linux (10.0.6.1) appartenant au VLAN Téléphones [7]

### 2. DHCP [100/0]

![alt text](Preuves/Preuve_DHCP_G4.png)
> Attribution automatique de l'adresse ipv4 de G4 via le serveur DHCP

### 3. NAT [0/100]

![alt text](Preuves/preuve_nat_S05.png)
> Ici le NAT permet de ping le routeur FAI et donc de sortir du réseau privé vers un réseau public

### 4. DNS [100/0]

![alt text](Preuves/Preuve_dns_G4.png)
> Premier ping vers dns2 : Il y a résolution de nom or aucune machine n'a l'ip donnée par le serveur DNS  
> Le second ping résoud le nom de domaine par l'adresse de la machine 

### 5. Serveur apache [100/0]
> Tous les tests ci dessous ont été effectués via G5 sur Linux en tant qu'employés.
#### Page publique
![alt text](Preuves/Preuve_WEB1.png)
*Cette page est accessible librement sur internet.*

#### Page Intra
![alt text](Preuves/Preuve_WEB_Intra.png)
*Cette page page demande une authentification par mot de passe.*

#### Page WAN
![alt text](Preuves/Preuve_WEB_WAN.png)
*Cette page est disponible uniquement sur le réseau privée.*

### 6. AD [100/0]

#### Groupes de sécurité & droits :

Le service n'étant pas fonctionnel aucune preuve ne pourra être donnée.

#### DNS_2

Par manque de temps dû au sous-effectif, le service DNS_2 n'a pas pu être connecté au réseau physique. 

---
<center>Ce dossier est réservé à l'équipe de Quentin D. & Louison R. ainsi qu'aux professeurs dans le cadre du Projet Réseaux.</center>
<center>Tous droits réservés</center>