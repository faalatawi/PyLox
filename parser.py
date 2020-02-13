import grammer
from tokentype import TokenType
import PyLox

class ParseError(Exception):
    """This is a parsing error"""
    pass 


class Parser(object):
    
    def __init__(self, tokens):
        self._tokens  = tokens
        self._current = 0

    def _expression(self):
        return self._equality()


    def _equality(self):
        """equality → comparison ( ( "!=" | "==" ) comparison )* """
        expr = self._comparison()

        match_list = [TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]
        while self._match(match_list) : 
            operator = self._previous()
            right = self._comparison()
            expr = grammer.Binary(expr, operator, right)
        
        return expr
    
    # comparison → addition ( ( ">" | ">=" | "<" | "<=" ) addition )* ;
    def _comparison(self):
        expr = self._addition()

        # GREATER, GREATER_EQUAL, LESS, LESS_EQUAL
        match_list = [TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL]
        while self._match(match_list) : 
            operator = self._previous()
            right = self._addition()
            expr = grammer.Binary(expr, operator, right)
        
        return expr
    
    def _addition(self):
        expr = self._multiplication()

        # MINUS, PLUS
        match_list = [TokenType.MINUS, TokenType.PLUS]
        while self._match(match_list) : 
            operator = self._previous()
            right = self._multiplication()
            expr = grammer.Binary(expr, operator, right)
        
        return expr
    
    def _multiplication(self):
        expr = self._unary()

        # SLASH, STAR
        match_list = [TokenType.SLASH, TokenType.STAR]
        while self._match(match_list):
            operator = self._previous()
            right = self._unary()
            expr = grammer.Binary(expr, operator, right)
        
        return expr

    # unary → ( "!" | "-" ) unary
    #       | primary ;
    def _unary(self):
        #BANG, MINUS
        match_list = [TokenType.BANG, TokenType.MINUS]
        if self._match(match_list):
            operator = self._previous()
            right = self._unary()
            return grammer.Unary(operator, right)
        
        return self._primary()

    # primary → NUMBER | STRING | "false" | "true" | "nil" | "(" expression ")" ;
    def _primary(self):

        if self._match([TokenType.FALSE]):
            return grammer.Literal(False)
        
        if self._match([TokenType.TRUE]):
            return grammer.Literal(True)
        
        if self._match([TokenType.NIL]):
            return grammer.Literal(None)
        
        # NUMBER, STRING
        if self._match([TokenType.NUMBER, TokenType.STRING]):
            value = self._previous().literal
            return grammer.Literal(value)

        
        if self._match([TokenType.LEFT_PAREN]) : 
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")

            return grammer.Grouping(expr)

    # ===================================================
    # Helping methods 

    def _consume(self, token, message):
        if self._check(token):
            return self._advance()
        
        raise self._error(token, message)

    def _error(self, token, message):
        PyLox.error_token(token, message) 

        return ParseError()

    def _match(self, match_list):
        for type in match_list:
            if self._check(type) :
                self._advance()
                return True
        
        return False

    def _check(self, token):
        if self._is_at_end():
            return False
        
        return self._peek() == token

    def _advance(self):
        if not self._is_at_end():
            self._current += 1

        return self._previous()    

    def _peek(self):
        return self._tokens[self._current]

    def _is_at_end(self):
        return self._peek() == TokenType.EOF

    def _previous(self):
        return self._tokens[self._current - 1]


