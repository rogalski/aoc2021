package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
)

type MostCommonElementTieError struct{}

func (m *MostCommonElementTieError) Error() string {
	return "Tie when looking for most common element"
}

func gammaRateEpsilonRateFromFilePath(path string) (int, int, error) {
	file, err := os.Open(path)
	if err != nil {
		return 0, 0, err
	}
	scanner := bufio.NewScanner(file)
	scanner.Scan()
	first := scanner.Text()
	numBits := len(first)
	counter := make([]int, len(first))
	file.Seek(0, io.SeekStart)
	scanner = bufio.NewScanner(file)
	for scanner.Scan() {
		for i := 0; i < numBits; i++ {
			count := 0
			if scanner.Bytes()[i] == '1' {
				count = 1
			} else {
				count = -1
			}
			counter[i] += count
		}
	}
	mask := 1<<(numBits) - 1
	gamma := 0
	for i := 0; i < numBits; i++ {
		if counter[i] == 0 {
			return 0, 0, err
		} else if counter[i] > 0 {
			// most common = 1
			gamma = gamma + 1<<(numBits-1-i)
		} else {
			// most common = 0, do nothing
		}
	}
	epsilon := mask ^ gamma
	return gamma, epsilon, nil
}

func Filter(slice []int, condition func(v int) bool) []int {
	filtered := make([]int, 0)
	for _, number := range slice {
		if condition(number) {
			filtered = append(filtered, number)
		}
	}
	return filtered
}

func GenericRatingFromFilePath(path string, preferMore bool) (int, error) {
	file, err := os.Open(path)
	if err != nil {
		return 0, err
	}
	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	scanner.Scan()
	first := scanner.Text()
	numBits := len(first)
	file.Seek(0, io.SeekStart)
	scanner = bufio.NewScanner(file)
	numbers := make([]int, 0)
	for scanner.Scan() {
		number, err := strconv.ParseInt(scanner.Text(), 2, 32)
		if err != nil {
			return 0, err
		}
		numbers = append(numbers, int(number))
	}
	// filtering for each bit
	for i := 0; i < numBits; i++ {
		mask := 1 << (numBits - 1 - i)
		countZeros := 0
		countOnes := 0
		for _, number := range numbers {
			if (number & mask) != 0 {
				countOnes += 1
			} else {
				countZeros += 1
			}
		}
		selectOnes := func(v int) bool { return (v & mask) > 0 }
		selectZeros := func(v int) bool { return (v & mask) == 0 }
		if preferMore {
			if countOnes >= countZeros {
				numbers = Filter(numbers, selectOnes)
			} else {
				numbers = Filter(numbers, selectZeros)
			}
		} else {
			if countOnes < countZeros {
				numbers = Filter(numbers, selectOnes)
			} else {
				numbers = Filter(numbers, selectZeros)
			}
		}
		if len(numbers) <= 1 {
			break
		}
	}
	return numbers[0], nil
}

func OxygenGeneratorRatingFromFilePath(path string) (int, error) {
	return GenericRatingFromFilePath(path, true)
}

func CO2ScrubberRatingFromFilePath(path string) (int, error) {
	return GenericRatingFromFilePath(path, false)
}

func main() {
	input := "input.txt"
	gamma, epsilon, err := gammaRateEpsilonRateFromFilePath(input)
	if err != nil {
		panic(err)
	}
	fmt.Printf("gamma: %v\n", gamma)
	fmt.Printf("epsilon: %v\n", epsilon)
	fmt.Printf("product: %v\n", gamma*epsilon)

	ogr, err := OxygenGeneratorRatingFromFilePath(input)
	if err != nil {
		panic(err)
	}
	co2r, err := CO2ScrubberRatingFromFilePath(input)
	if err != nil {
		panic(err)
	}
	fmt.Printf("ogr: %v\n", ogr)
	fmt.Printf("co2r: %v\n", co2r)
	fmt.Printf("product: %v\n", ogr*co2r)
}
