package com.spe.calculator.service;

import com.spe.calculator.exception.DivisionByZeroException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for {@link CalculatorService}.
 *
 * <p>No Spring context is loaded — the service is instantiated directly,
 * making these tests fast and independent of infrastructure.
 */
@DisplayName("CalculatorService Unit Tests")
class CalculatorServiceTest {

    private CalculatorService calculatorService;

    @BeforeEach
    void setUp() {
        calculatorService = new CalculatorService();
    }

    // ------------------------------------------------------------------ ADD
    @Test
    @DisplayName("add: positive numbers")
    void add_positiveNumbers_returnsSum() {
        assertEquals(8.0, calculatorService.add(5.0, 3.0), 1e-9);
    }

    @Test
    @DisplayName("add: negative numbers")
    void add_negativeNumbers_returnsSum() {
        assertEquals(-8.0, calculatorService.add(-5.0, -3.0), 1e-9);
    }

    @Test
    @DisplayName("add: one operand is zero")
    void add_withZero_returnsOtherOperand() {
        assertEquals(7.0, calculatorService.add(7.0, 0.0), 1e-9);
    }

    // ------------------------------------------------------------ SUBTRACT
    @Test
    @DisplayName("subtract: positive numbers")
    void subtract_positiveNumbers_returnsDifference() {
        assertEquals(2.0, calculatorService.subtract(5.0, 3.0), 1e-9);
    }

    @Test
    @DisplayName("subtract: result is negative")
    void subtract_smallerFromLarger_returnsNegative() {
        assertEquals(-2.0, calculatorService.subtract(3.0, 5.0), 1e-9);
    }

    @Test
    @DisplayName("subtract: same numbers returns zero")
    void subtract_sameNumbers_returnsZero() {
        assertEquals(0.0, calculatorService.subtract(4.0, 4.0), 1e-9);
    }

    // ------------------------------------------------------------ MULTIPLY
    @Test
    @DisplayName("multiply: positive numbers")
    void multiply_positiveNumbers_returnsProduct() {
        assertEquals(15.0, calculatorService.multiply(3.0, 5.0), 1e-9);
    }

    @Test
    @DisplayName("multiply: by zero returns zero")
    void multiply_byZero_returnsZero() {
        assertEquals(0.0, calculatorService.multiply(99.0, 0.0), 1e-9);
    }

    @Test
    @DisplayName("multiply: negative times negative is positive")
    void multiply_twoNegatives_returnsPositive() {
        assertEquals(6.0, calculatorService.multiply(-2.0, -3.0), 1e-9);
    }

    // -------------------------------------------------------------- DIVIDE
    @Test
    @DisplayName("divide: positive numbers")
    void divide_positiveNumbers_returnsQuotient() {
        assertEquals(2.5, calculatorService.divide(5.0, 2.0), 1e-9);
    }

    @Test
    @DisplayName("divide: exact integer division")
    void divide_exactDivision_returnsWholeNumber() {
        assertEquals(4.0, calculatorService.divide(12.0, 3.0), 1e-9);
    }

    @Test
    @DisplayName("divide: by zero throws DivisionByZeroException")
    void divide_byZero_throwsDivisionByZeroException() {
        DivisionByZeroException ex = assertThrows(
                DivisionByZeroException.class,
                () -> calculatorService.divide(10.0, 0.0)
        );
        assertEquals("Division by zero is not allowed", ex.getMessage());
        assertEquals(10.0, ex.getA(), 1e-9);
        assertEquals(0.0,  ex.getB(), 1e-9);
    }

    @Test
    @DisplayName("divide: negative dividend by positive divisor")
    void divide_negativeDividend_returnsNegativeQuotient() {
        assertEquals(-3.0, calculatorService.divide(-9.0, 3.0), 1e-9);
    }
}
