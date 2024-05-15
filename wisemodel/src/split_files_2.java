import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.nio.channels.FileChannel;

public class FileSplitter {
    public static void splitFile(String sourceFile, int blockSize) {
        try (FileInputStream fis = new FileInputStream(sourceFile);
             FileChannel sourceChannel = fis.getChannel()) {
            long fileSize = sourceChannel.size();
            long position = 0;
            int partNum = 1;
            while (position < fileSize) {
                try (FileOutputStream fos = new FileOutputStream(sourceFile + "_part" + partNum);
                     FileChannel destChannel = fos.getChannel()) {
                    long transferred = sourceChannel.transferTo(position, blockSize, destChannel);
                    position += transferred;
                    partNum++;
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        splitFile("path_to_large_file.dat", 1024 * 1024 * 10); // 切分为10MB大小的块
    }
}