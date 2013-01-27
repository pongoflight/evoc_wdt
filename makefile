
evoc_wdt:
	gcc -fPIC -shared -DDYNAMIC -o evoc_wdt.so evoc_wdt.c
	gcc -o evoc_wdt evoc_wdt.c

clean:
	rm -f evoc_wdt.so evoc_wdt
