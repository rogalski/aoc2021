package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func readInt(scanner bufio.Scanner) (int, error) {
	if err := scanner.Err(); err != nil {
		return 0, err
	}
	value, err := strconv.Atoi(scanner.Text())
	if err != nil {
		return 0, err
	}
	return value, nil
}

func depthIncreaseCount(path string) (int, error) {
	file, err := os.Open(path)
	if err != nil {
		return 0, err
	}
	defer file.Close()

	var count = 0

	scanner := bufio.NewScanner(file)
	scanner.Scan()
	prev, err := readInt(*scanner)
	if err != nil {
		return 0, err
	}
	for scanner.Scan() {
		next, err := readInt(*scanner)
		if err != nil {
			return 0, nil
		}
		if next > prev {
			count = count + 1
		}
		prev = next
	}
	return count, nil
}

func depthIncreaseCountWithSlidingWindow(path string, size int) (int, error) {
	file, err := os.Open(path)
	if err != nil {
		return 0, err
	}
	defer file.Close()

	var count = 0

	scanner := bufio.NewScanner(file)

	window := make([]int, size)
	for i := 0; i < size; i++ {
		scanner.Scan()
		item, err := readInt(*scanner)
		if err != nil {
			return 0, err
		}
		window[i] = item
	}

	for scanner.Scan() {
		item, err := readInt(*scanner)
		if err != nil {
			return 0, nil
		}
		if item > window[0] {
			count = count + 1
		}
		// shift window
		for i := 1; i < size; i++ {
			window[i-1] = window[i]
		}
		window[size-1] = item
	}
	return count, nil
}

func main() {
	filename := os.Args[1]
	count, err := depthIncreaseCount(filename)
	if err != nil {
		panic(err)
	}
	fmt.Println("depthIncreaseCount", count)
	count, err = depthIncreaseCountWithSlidingWindow(filename, 3)
	if err != nil {
		panic(err)
	}
	fmt.Println("depthIncreaseCountWithSlidingWindow", count)
}
