import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.printer.DotPrinter;
import com.github.javaparser.utils.Pair;

import java.io.*;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static java.lang.Math.max;

// Testing pass on Windows 10, JDK12
public class Main {
    static void saveToDot(String filePath, String FILE_NAME) throws Exception {
        CompilationUnit cu = StaticJavaParser.parse(new File(filePath + "/" + FILE_NAME));

        DotPrinter printer = new DotPrinter(true);
        try (FileWriter fileWriter = new FileWriter(filePath + "/" + FILE_NAME + ".dot"); PrintWriter printWriter = new PrintWriter(fileWriter)) {
            printWriter.print(printer.output(cu));
        }
    }

    static void saveEdge(ArrayList<Pair<Integer, Integer>> parseResult, String filePath, String fileName) throws IOException {
        BufferedWriter out = new BufferedWriter(new FileWriter(filePath + "/" + fileName));
        for (Pair<Integer, Integer> item : parseResult) {
            out.write(String.format("%d,%d\n", item.a, item.b));
        }
        out.close();
    }

    static int[][] transMatrix(ArrayList<Pair<Integer, Integer>> parseResult, int MAX_VEX_NUMBER) {
        int[][] arc = new int[MAX_VEX_NUMBER][MAX_VEX_NUMBER];
        for (Pair<Integer, Integer> item : parseResult) {
            arc[item.a][item.b] = 1;
        }
        return arc;
    }

    static boolean checkIsGraphPath(String str) {
        Pattern pattern = Pattern.compile("^n(.*)->(.*);");
        Matcher match = pattern.matcher(str);
        return match.matches();
    }

    static Pair<Integer, Integer> parseGraphPath(String str) {
        Matcher matcher = Pattern.compile("[0-9]+").matcher(str);
        int matcher_start = 0;
        int first = 1, result1 = -1, result2 = -1;
        while (matcher.find(matcher_start)) {
            if (first == 1) {
                first = 0;
                result1 = Integer.parseInt(matcher.group(0));
            } else {
                result2 = Integer.parseInt(matcher.group(0));
            }
            matcher_start = matcher.end();
        }
        return new Pair<>(result1, result2);
    }

    static void generateDot(String FILE_PATH) throws Exception {
        File file = new File(FILE_PATH);
        File[] fs = file.listFiles();
        for (File f : fs) {
            if (f.isFile() && f.toString().endsWith(".java")) {
                saveToDot(FILE_PATH, f.getName());
            }
        }
    }

    static void generateGraphData(String filePath) throws Exception {
        File file = new File(filePath);
        File[] fs = file.listFiles();
        assert fs != null;
        for (File f : fs) {
            if (f.isFile() && f.toString().endsWith(".dot")) {
                System.out.printf("=== Parsing file: %s ... ===\n", f);
                int MAX_VEX_NUMBER = 0;
                ArrayList<Pair<Integer, Integer>> parseResult = new ArrayList<>();
                try (BufferedReader br = new BufferedReader(new FileReader(f))) {
                    String line;
                    while ((line = br.readLine()) != null) {
                        if (checkIsGraphPath(line)) {
                            Pair<Integer, Integer> UV = parseGraphPath(line);
                            parseResult.add(UV);
                            MAX_VEX_NUMBER = max(MAX_VEX_NUMBER, max(UV.a, UV.b));
//                            System.out.printf("u:%d v:%d\n", UV.a, UV.b);
                        }
                    }
                    // 调用该方法将会把AST对应的边写入文件中
                    saveEdge(parseResult, filePath, f.getName() + ".txt");
                    // 如需要01矩阵，可调用该方法获得一个处理完毕的二维数组，而后将其写入文件即可
                    // transMatrix(parseResult, MAX_VEX_NUMBER + 1);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public static void main(String[] args) throws Exception {
        // 源代码存放目录
        String FILE_PATH = "E:\\JFinder\\data\\slice";
//        String FILE_PATH = "E:\\JFinder\\paper_exp\\output\\tmp\\slice";
        // 代码转存为Dot绘图文件
        generateDot(FILE_PATH);
        // Dot绘图文件转换为<u, v>，代表连边
        generateGraphData(FILE_PATH);
    }
}

