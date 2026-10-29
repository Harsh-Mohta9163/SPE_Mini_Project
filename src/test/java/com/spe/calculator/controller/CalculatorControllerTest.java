package com.spe.calculator.controller;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Integration tests for {@link CalculatorController} using MockMvc.
 *
 * <p>Loads the full Spring application context ({@code @SpringBootTest})
 * and exercises the real HTTP layer including request mapping,
 * parameter binding, JSON serialisation, and exception handling.
 */
@SpringBootTest
@AutoConfigureMockMvc
@DisplayName("CalculatorController Integration Tests")
class CalculatorControllerTest {

    @Autowired
    private MockMvc mockMvc;

    // ------------------------------------------------------------------ ADD
    @Test
    @DisplayName("GET /api/v1/add?a=2&b=3 → 200, result=5")
    void add_validParams_returns200WithResult() throws Exception {
        mockMvc.perform(get("/api/v1/add")
                        .param("a", "2")
                        .param("b", "3")
                        .accept(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.operation").value("add"))
                .andExpect(jsonPath("$.a").value(2.0))
                .andExpect(jsonPath("$.b").value(3.0))
                .andExpect(jsonPath("$.result").value(5.0));
    }

    @Test
    @DisplayName("GET /api/v1/add with negative numbers → 200")
    void add_negativeNumbers_returns200() throws Exception {
        mockMvc.perform(get("/api/v1/add")
                        .param("a", "-5")
                        .param("b", "-3"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").value(-8.0));
    }

    // ------------------------------------------------------------ SUBTRACT
    @Test
    @DisplayName("GET /api/v1/subtract?a=10&b=4 → 200, result=6")
    void subtract_validParams_returns200WithResult() throws Exception {
        mockMvc.perform(get("/api/v1/subtract")
                        .param("a", "10")
                        .param("b", "4"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.operation").value("subtract"))
                .andExpect(jsonPath("$.result").value(6.0));
    }

    // ------------------------------------------------------------ MULTIPLY
    @Test
    @DisplayName("GET /api/v1/multiply?a=6&b=7 → 200, result=42")
    void multiply_validParams_returns200WithResult() throws Exception {
        mockMvc.perform(get("/api/v1/multiply")
                        .param("a", "6")
                        .param("b", "7"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.operation").value("multiply"))
                .andExpect(jsonPath("$.result").value(42.0));
    }

    // -------------------------------------------------------------- DIVIDE
    @Test
    @DisplayName("GET /api/v1/divide?a=10&b=2 → 200, result=5")
    void divide_validParams_returns200WithResult() throws Exception {
        mockMvc.perform(get("/api/v1/divide")
                        .param("a", "10")
                        .param("b", "2"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.operation").value("divide"))
                .andExpect(jsonPath("$.result").value(5.0));
    }

    @Test
    @DisplayName("GET /api/v1/divide?a=10&b=0 → 400 with error body")
    void divide_byZero_returns400WithErrorBody() throws Exception {
        mockMvc.perform(get("/api/v1/divide")
                        .param("a", "10")
                        .param("b", "0"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").value("Division by zero is not allowed"))
                .andExpect(jsonPath("$.a").value(10.0))
                .andExpect(jsonPath("$.b").value(0.0));
    }

    // ----------------------------------------------------- ERROR HANDLING
    @Test
    @DisplayName("GET /api/v1/add with missing param b → 400")
    void add_missingParam_returns400() throws Exception {
        mockMvc.perform(get("/api/v1/add")
                        .param("a", "5"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").exists());
    }

    @Test
    @DisplayName("GET /api/v1/add with non-numeric param → 400")
    void add_nonNumericParam_returns400() throws Exception {
        mockMvc.perform(get("/api/v1/add")
                        .param("a", "abc")
                        .param("b", "3"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").exists());
    }

    // ------------------------------------------------------------ ACTUATOR
    @Test
    @DisplayName("GET /actuator/health → 200 UP")
    void actuatorHealth_returns200Up() throws Exception {
        mockMvc.perform(get("/actuator/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"));
    }
}
