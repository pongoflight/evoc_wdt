
evoc_wdt:evoc_wdt.o
	gcc -o evoc_wdt evoc_wdt.o

evoc_wdt.o:evoc_wdt.c
	gcc -c -w -o evoc_wdt.o evoc_wdt.c

clean:
	rm -f evoc_wdt.o evoc_wdt
