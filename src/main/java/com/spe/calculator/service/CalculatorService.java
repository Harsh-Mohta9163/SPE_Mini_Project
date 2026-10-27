package com.spe.calculator.service;

import com.spe.calculator.exception.DivisionByZeroException;
import org.springframework.stereotype.Service;

/**
 * Business logic layer for all calculator operations.
 *
 * <p>Keeps arithmetic concerns separate from HTTP/controller concerns,
 * making this class easy to unit-test without starting a Spring context.
 *
 * <p>Throws {@link DivisionByZeroException} when the divisor is zero;
 * the {@code GlobalExceptionHandler} maps this to HTTP 400.
 */
@Service
public class CalculatorService {

    /**
     * Adds two numbers.
     *
     * @param a first operand
     * @param b second operand
     * @return a + b
     */
    public double add(double a, double b) {
        return a + b;
    }

    /**
     * Subtracts b from a.
     *
     * @param a first operand
     * @param b second operand
     * @return a - b
     */
    public double subtract(double a, double b) {
        return a - b;
    }

    /**
     * Multiplies two numbers.
     *
     * @param a first operand
     * @param b second operand
     * @return a * b
     */
    public double multiply(double a, double b) {
        return a * b;
    }

    /**
     * Divides a by b.
     *
     * @param a dividend
     * @param b divisor — must not be zero
     * @return a / b
     * @throws DivisionByZeroException if b == 0
     */
    public double divide(double a, double b) {
        if (b == 0) {
            throw new DivisionByZeroException(
                    "Division by zero is not allowed", a, b);
        }
        return a / b;
    }
}
