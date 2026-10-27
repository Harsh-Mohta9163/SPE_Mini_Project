package com.spe.calculator.exception;

import com.spe.calculator.dto.ErrorResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;

/**
 * Centralised error handler for the Calculator REST API.
 *
 * <p>Intercepts exceptions thrown from controllers and services and
 * converts them into structured JSON error responses with appropriate
 * HTTP status codes, keeping controller code clean and consistent.
 *
 * <p>Handled cases:
 * <ul>
 *   <li>{@link DivisionByZeroException}                   → 400 Bad Request</li>
 *   <li>{@link MissingServletRequestParameterException}   → 400 Bad Request</li>
 *   <li>{@link MethodArgumentTypeMismatchException}        → 400 Bad Request</li>
 * </ul>
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * Handles division by zero; returns 400 with the offending operands.
     */
    @ExceptionHandler(DivisionByZeroException.class)
    public ResponseEntity<ErrorResponse> handleDivisionByZero(DivisionByZeroException ex) {
        ErrorResponse body = new ErrorResponse(ex.getMessage(), ex.getA(), ex.getB());
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(body);
    }

    /**
     * Handles missing query parameters (e.g. ?a= without &b=).
     */
    @ExceptionHandler(MissingServletRequestParameterException.class)
    public ResponseEntity<ErrorResponse> handleMissingParam(
            MissingServletRequestParameterException ex) {
        ErrorResponse body = new ErrorResponse(
                "Missing required parameter: " + ex.getParameterName(), 0, 0);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(body);
    }

    /**
     * Handles non-numeric parameter values (e.g. ?a=abc).
     */
    @ExceptionHandler(MethodArgumentTypeMismatchException.class)
    public ResponseEntity<ErrorResponse> handleTypeMismatch(
            MethodArgumentTypeMismatchException ex) {
        ErrorResponse body = new ErrorResponse(
                "Invalid value for parameter '" + ex.getName()
                        + "': must be a number", 0, 0);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(body);
    }
}
