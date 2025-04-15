## After clone, run:

### Create Docker Environment 
- chmod +x dockersetup
- ./dockersetup
- sudo bash
- docker compose up -d

### Configure Host Routs  
- docker exec -it part15-ha-1 ip route del default
- docker exec -it part15-ha-1 ip route add default via 10.0.14.4

- docker exec -it part15-hb-1 ip route del default
- docker exec -it part15-hb-1 ip route add default via 10.0.15.4
