fonction1(x,y){
    var t1[4];
    t1[0] = 1;
    while(y) {
        printf(y);
        z = fonction2(x, y);
    }
    return (x+y);
}
fonction2(x,y){
    return (x-y);
}
main(x,y){
    while(x) {
        y = y + 1;
        z = fonction1(x,y);
        printf(z);
    }
    return (y);
}