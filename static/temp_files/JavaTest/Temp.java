import java.util.*;

public class Temp{
    public static long fibonacci(int n) {
        if (n <= 1) return n;
        else return fibonacci(n-1) + fibonacci(n-2);
    }

    public static void main(String[] args) {
	  	Scanner girdi = new Scanner(System.in);
	    int n=girdi.nextInt();
	  
        for (int i = 1; i <= n; i++)
            System.out.println(fibonacci(i) + "\n");
    }

}
