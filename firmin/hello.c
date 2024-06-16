fonction1(x,y){
    return (x+y);
}
fonction2(x,y){
    return (x*y);
}
main(X, Y){
    while(X){
        X=X-1;
        Y=Y+1;
        Z=fonction1(X,Y);
        printf(Z);
    }
    return (Y);
}