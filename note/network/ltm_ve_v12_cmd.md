##### show the health of RAID array hard drives
```
root@(bigip12ve)(cfg-sync Standalone)(Active)(/Common)(tmos)# show /sys raid disk

-------------------------------------------------------------------
Sys::Raid::Disk
Name  Serial Number  Array   Array Status  Model
                     Member                 
-------------------------------------------------------------------
HD1   VMware-sda     no      undefined     VMware, VMware Virtual S
HD2   VMware-sdb     no      undefined     VMware, VMware Virtual S
```

```
root@(bigip12ve)(cfg-sync Standalone)(Active)(/Common)(tmos)# show /cm traffic-group 
                                                                                                                                                                                               
-------------------------------------------------------------
CM::Traffic-Group       
Name                      Device               Status  Next
                                                       Active
-------------------------------------------------------------
traffic-group-1           bigip12ve.localhost  active  false
traffic-group-local-only  - 

```


