package main

import (
	"bufio"
	"os"
	"strconv"
	"strings"
)

type UnsupportedCmdError struct{}

func (m *UnsupportedCmdError) Error() string {
	return "Unsupported cmd"
}

func finalPositionAndDepth(filePath string) (int, int, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return 0, 0, err
	}
	defer file.Close()
	position := 0
	depth := 0
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		split := strings.Fields(line)
		command := split[0]
		value, err := strconv.Atoi(split[1])
		if err != nil {
			return 0, 0, err
		}
		if command == "forward" {
			position = position + value
		} else if command == "down" {
			depth = depth + value
		} else if command == "up" {
			depth = depth - value
		} else {
			return 0, 0, &UnsupportedCmdError{}
		}

	}
	return position, depth, nil
}

func finalPositionAndDepthWithAim(filePath string) (int, int, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return 0, 0, err
	}
	defer file.Close()
	position := 0
	depth := 0
	aim := 0
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		split := strings.Fields(line)
		command := split[0]
		value, err := strconv.Atoi(split[1])
		if err != nil {
			return 0, 0, err
		}
		if command == "forward" {
			position = position + value
			depth = depth + (aim * value)
		} else if command == "down" {
			aim = aim + value
		} else if command == "up" {
			aim = aim - value
		} else {
			return 0, 0, &UnsupportedCmdError{}
		}

	}
	return position, depth, nil
}

func main() {
	position, depth, err := finalPositionAndDepth(os.Args[1])
	if err != nil {
		panic(err)
	}
	println(position * depth)
	position, depth, err = finalPositionAndDepthWithAim(os.Args[1])
	if err != nil {
		panic(err)
	}
	println(position * depth)
}
