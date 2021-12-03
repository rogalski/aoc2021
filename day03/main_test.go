package main

import (
	"fmt"
	"testing"
)

func TestGammaRateEpsilonRateFromFilePath(t *testing.T) {
	gamma, epsilon, err := gammaRateEpsilonRateFromFilePath("ex.txt")
	fmt.Printf("gamma: %v\n", gamma)
	fmt.Printf("epsilon: %v\n", epsilon)
	if err != nil {
		t.Errorf(err.Error())
	}
	if gamma != 22 {
		t.Errorf("gamma was %d", gamma)
	}
	if epsilon != 9 {
		t.Errorf("epsilon was %d", epsilon)
	}
}

func TestOxygenGeneratorRatingFromFilePath(t *testing.T) {
	ogr, err := OxygenGeneratorRatingFromFilePath("ex.txt")
	if err != nil {
		t.Errorf(err.Error())
	}
	if ogr != 23 {
		t.Errorf("oxygen generator rating was %d", ogr)
	}
}
func TestCO2ScrubberRatingFromFilePath(t *testing.T) {
	co2r, err := CO2ScrubberRatingFromFilePath("ex.txt")
	if err != nil {
		t.Errorf(err.Error())
	}
	if co2r != 10 {
		t.Errorf("co2 scribber rating was %d", co2r)
	}
}
