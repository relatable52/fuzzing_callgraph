import com.code_intelligence.jazzer.api.FuzzedDataProvider;

import net.sf.jsqlparser.JSQLParserException;
import net.sf.jsqlparser.parser.CCJSqlParserUtil;
import net.sf.jsqlparser.parser.TokenMgrException;

class JSqlParserFuzzer {
    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
        String simpleSql = data.consumeString(1000);
        String sqlScript = data.consumeString(1000);
        String expression = data.consumeString(1000);
        String ast = data.consumeString(1000);
        String condExp = data.consumeString(1000);
        try{
            try {
                CCJSqlParserUtil.parse(
                        simpleSql,
                        parser -> parser
                                .withSquareBracketQuotation(data.consumeBoolean())
                                .withAllowComplexParsing(data.consumeBoolean())
                                .withUnsupportedStatements(data.consumeBoolean())
                                .withBackslashEscapeCharacter(data.consumeBoolean())
                );
            } catch (JSQLParserException e) {
            }
    
            try {
                CCJSqlParserUtil.parseStatements(
                        sqlScript,
                        parser -> parser
                                .withSquareBracketQuotation(data.consumeBoolean())
                                .withAllowComplexParsing(data.consumeBoolean())
                                .withUnsupportedStatements(data.consumeBoolean())
                                .withBackslashEscapeCharacter(data.consumeBoolean())
                );
            } catch (JSQLParserException e) {
            }
    
            try {
                CCJSqlParserUtil.parseAST(ast);
            } catch (JSQLParserException e) {
            }
    
            try {
                CCJSqlParserUtil.parseExpression(
                        expression,
                        data.consumeBoolean(),
                        parser -> parser
                                .withSquareBracketQuotation(data.consumeBoolean())
                                .withAllowComplexParsing(data.consumeBoolean())
                                .withUnsupportedStatements(data.consumeBoolean())
                                .withBackslashEscapeCharacter(data.consumeBoolean())
                );
            } catch (JSQLParserException e) {
            } catch (ArrayIndexOutOfBoundsException | TokenMgrException e) {
                // Needed to catch to enable fuzzer to continue
            }
    
            try {
                CCJSqlParserUtil.parseCondExpression(
                        condExp,
                        data.consumeBoolean(),
                        parser -> parser
                                .withSquareBracketQuotation(data.consumeBoolean())
                                .withAllowComplexParsing(data.consumeBoolean())
                                .withUnsupportedStatements(data.consumeBoolean())
                                .withBackslashEscapeCharacter(data.consumeBoolean())
                );
            } catch (JSQLParserException e) {
            } catch (ArrayIndexOutOfBoundsException | TokenMgrException e) {
                // Needed to catch to enable fuzzer to continue
            }
        } catch (Exception e) {}
    }
}