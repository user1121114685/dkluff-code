package main

import ("fmt"
        "log"
        "net/http"
        "flag"
        "strings"
        "os"
)
var html, ipaddr *string 
func rqdef(w http.ResponseWriter, r *http.Request) {
    f,err := os.Open(*html)
    if err != nil {
        fmt.Println(err)
    }
    data := make([]byte,100)
    count,err := f.Read(data)
    if err != nil {
        fmt.Println(err)
    }
    fmt.Fprintf(w, strings.Join([]string{*ipaddr,":",string(data[:count])},""))
    fmt.Println(*ipaddr)
}
func main() {
    ipaddr = flag.String("i", "", "http listen addr")
    html = flag.String("f","def.html","html content")
    flag.Parse()
    fmt.Println("running on ip: ",*ipaddr)
    ipp := strings.Join([]string{*ipaddr, ":80"}, "")

    http.HandleFunc("/",rqdef)
    log.Fatal(http.ListenAndServe(ipp, nil))
}
