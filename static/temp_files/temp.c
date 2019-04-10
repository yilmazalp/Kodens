#include<stdio.h>
#include<conio.h>

int f(n){
  if(n==1){
	return 1;
  }
  
  else if(n>1){
	return f(n-1) + f(n-2);
  }
}

int main(){
  int sayi;
  scanf("%d", &sayi);
  int k;
  
  for(k=1; k <=sayi; k++){
	if(f(k)%2==0){
	  printf("%d\n", f(k));
	}
  }
  
  return 0;
}
	
	
	
	
	
	