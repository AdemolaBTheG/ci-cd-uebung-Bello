package com.example.cicd;

import org.junit.jupiter.api.Test;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Hinweise:
 * - Ergänze weitere Testfälle (z. B. negative Zahlen, große Werte)
 * - Diskutiere das Verhalten von divide(… , 0) und entscheide in Ü2, ob Exception sinnvoller ist
 */
class CalculatorTest {

    @Test
    void add_shouldSumTwoIntegers() {
        Calculator c = new Calculator();
        assertEquals(5, c.add(2, 3));
    }

    @Test
    void add_negativeNumbers_shouldReturnNegativeSum() {
        Calculator c = new Calculator();
        assertEquals(-8, c.add(-3, -5));
    }

    @Test
    void subtract_largerNumber_shouldReturnNegativeDifference() {
        Calculator c = new Calculator();
        assertEquals(-5, c.subtract(3, 8));
    }

    @Test
    void divide_nonDivisibleNumbers_shouldTruncateTowardsZero() {
        Calculator c = new Calculator();
        assertEquals(-3, c.divide(-10, 3));
    }

    @Test
    void sum_methods_emptyList_shouldReturnZero() {
        Calculator c = new Calculator();
        assertEquals(0, c.sumUp(List.of()));
        assertEquals(0, c.addAll(List.of()));
    }

    @Test
    void sum_methods_withNullsAndNegativeNumbers_shouldReturnExpectedSum() {
        Calculator c = new Calculator();
        List<Integer> nums = Arrays.asList(null, -5, 2, null, 10);
        assertEquals(7, c.sumUp(nums));
        assertEquals(7, c.addAll(nums));
    }

    @Test
    void divide_byZero_shouldReturnZero_currentBehavior() {
        Calculator c = new Calculator();
        // Aktuelles (schlechtes) Verhalten absichtlich bestätigt – Refactoring in Ü2
        assertEquals(0, c.divide(10, 0));
    }

    @Test
    void sum_methods_shouldProduceSameResult() {
        Calculator c = new Calculator();
        List<Integer> nums = Arrays.asList(1, 2, 3, null, 4);
        assertEquals(c.sumUp(nums), c.addAll(nums));
    }
}
