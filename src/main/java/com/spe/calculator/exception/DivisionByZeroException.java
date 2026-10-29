package com.spe.calculator.exception;

/**
 * Thrown by {@code CalculatorService} when a division by zero is attempted.
 *
 * <p>Carries the original operands so the {@code GlobalExceptionHandler}
 * can include them in the HTTP 400 error response body.
 */
public class DivisionByZeroException extends RuntimeException {

    private final double a;
    private final double b;

    public DivisionByZeroException(String message, double a, double b) {
        super(message);
        this.a = a;
        this.b = b;
    }

    public double getA() { return a; }
    public double getB() { return b; }
}
