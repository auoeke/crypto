package main

import (
	"flag"
	"fmt"
	"log"
	"os"
)

func xor(args []string) string {
	switch {
	case len(args) == 0:
		return ""
	case len(args) == 1:
		return args[0]
	case len(args) >= 2:
		if len(args[0]) == len(args[1]) {
			var result string
			for index := range args[0] {
				result += string(args[0][index] ^ args[1][index])
			}
			args = append(args[2:], result)
		} else {
			log.Fatal("Error: arguments are of different lengths.")
		}
	}
	return xor(args)
}

func main() {
	//bin := flag.Bool("b", true, "treats binary arguments as binary values")
	file := flag.String("f", "string", "accepts files as arguments")
	flag.Parse()
	fmt.Println(*file)
	text, err := os.Open(*file)
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(*text)
	}
	fmt.Println(xor(flag.Args()))
}
