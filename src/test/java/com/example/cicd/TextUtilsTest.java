package com.example.cicd;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/** Regressionstests für die in Übung 2 behobenen Fehler. */
class TextUtilsTest {

    @Test
    void safeParseInt_validNumber_returnsValue() {
        assertEquals(42, TextUtils.safeParseInt("42"));
    }

    @Test
    void safeParseInt_invalidNumber_returnsZero() {
        assertEquals(0, TextUtils.safeParseInt("x"));
    }

    @Test
    void isPalindrome_caseInsensitive_expectedTrue() {
        assertTrue(TextUtils.isPalindrome("Anna"));
    }

    @Test
    void safeParseInt_negativeNumber_returnsValue() {
        assertEquals(-17, TextUtils.safeParseInt("-17"));
    }

    @Test
    void safeParseInt_outOfIntegerRange_returnsZero() {
        assertEquals(0, TextUtils.safeParseInt("2147483648"));
    }

    @Test
    void isPalindrome_null_returnsFalse() {
        assertFalse(TextUtils.isPalindrome(null));
    }

    @Test
    void isPalindrome_nonPalindrome_returnsFalse() {
        assertFalse(TextUtils.isPalindrome("Java"));
    }

    @Test
    void isPalindrome_emptyAndSingleCharacter_returnsTrue() {
        assertTrue(TextUtils.isPalindrome(""));
        assertTrue(TextUtils.isPalindrome("a"));
    }

    @Test
    void safeParseInt_nullAndEmpty_returnsZero() {
        assertEquals(0, TextUtils.safeParseInt(null));
        assertEquals(0, TextUtils.safeParseInt(""));
    }

    @Test
    void safeParseInt_integerLimits_returnsValue() {
        assertEquals(Integer.MIN_VALUE, TextUtils.safeParseInt("-2147483648"));
        assertEquals(Integer.MAX_VALUE, TextUtils.safeParseInt("2147483647"));
    }
}
