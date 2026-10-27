package com.spe.calculator.dto;

/**
 * Error response returned for invalid inputs or illegal operations.
 *
 * <p>Returned with HTTP 400 Bad Request. Example JSON:
 * <pre>
 * {
 *   "error": "Division by zero is not allowed",
 *   "a": 10.0,
 *   "b": 0.0
 * }
 * </pre>
 */
public class ErrorResponse {

    private String error;
    private double a;
    private double b;

    public ErrorResponse() {}

    public ErrorResponse(String error, double a, double b) {
        this.error = error;
        this.a = a;
        this.b = b;
    }

    public String getError() { return error; }
    public void setError(String error) { this.error = error; }

    public double getA() { return a; }
    public void setA(double a) { this.a = a; }

    public double getB() { return b; }
    public void setB(double b) { this.b = b; }
}
