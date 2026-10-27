package com.spe.calculator.controller;

import com.spe.calculator.dto.CalculatorResponse;
import com.spe.calculator.service.CalculatorService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * REST controller exposing calculator operations under /api/v1.
 *
 * <p>All endpoints accept query parameters {@code a} and {@code b} as
 * doubles and return a {@link CalculatorResponse} JSON body on success.
 * Invalid/missing parameters produce an HTTP 400 via Spring's built-in
 * type-conversion failure, and division by zero is handled by
 * {@code GlobalExceptionHandler}.
 *
 * <p>Endpoints:
 * <ul>
 *   <li>GET /api/v1/add?a=&amp;b=</li>
 *   <li>GET /api/v1/subtract?a=&amp;b=</li>
 *   <li>GET /api/v1/multiply?a=&amp;b=</li>
 *   <li>GET /api/v1/divide?a=&amp;b=</li>
 * </ul>
 */
@RestController
@RequestMapping("/api/v1")
public class CalculatorController {

    private final CalculatorService calculatorService;

    public CalculatorController(CalculatorService calculatorService) {
        this.calculatorService = calculatorService;
    }

    /**
     * GET /api/v1/add?a={a}&b={b}
     *
     * @param a first operand
     * @param b second operand
     * @return HTTP 200 with JSON body containing a + b
     */
    @GetMapping("/add")
    public ResponseEntity<CalculatorResponse> add(
            @RequestParam double a,
            @RequestParam double b) {
        double result = calculatorService.add(a, b);
        return ResponseEntity.ok(new CalculatorResponse("add", a, b, result));
    }

    /**
     * GET /api/v1/subtract?a={a}&b={b}
     *
     * @param a first operand
     * @param b second operand
     * @return HTTP 200 with JSON body containing a - b
     */
    @GetMapping("/subtract")
    public ResponseEntity<CalculatorResponse> subtract(
            @RequestParam double a,
            @RequestParam double b) {
        double result = calculatorService.subtract(a, b);
        return ResponseEntity.ok(new CalculatorResponse("subtract", a, b, result));
    }

    /**
     * GET /api/v1/multiply?a={a}&b={b}
     *
     * @param a first operand
     * @param b second operand
     * @return HTTP 200 with JSON body containing a * b
     */
    @GetMapping("/multiply")
    public ResponseEntity<CalculatorResponse> multiply(
            @RequestParam double a,
            @RequestParam double b) {
        double result = calculatorService.multiply(a, b);
        return ResponseEntity.ok(new CalculatorResponse("multiply", a, b, result));
    }

    /**
     * GET /api/v1/divide?a={a}&b={b}
     *
     * @param a dividend
     * @param b divisor (must not be 0)
     * @return HTTP 200 with JSON body containing a / b,
     *         or HTTP 400 if b == 0
     */
    @GetMapping("/divide")
    public ResponseEntity<CalculatorResponse> divide(
            @RequestParam double a,
            @RequestParam double b) {
        double result = calculatorService.divide(a, b);
        return ResponseEntity.ok(new CalculatorResponse("divide", a, b, result));
    }
}
