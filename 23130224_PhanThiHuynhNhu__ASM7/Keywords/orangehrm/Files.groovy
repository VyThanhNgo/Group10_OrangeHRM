package orangehrm

import java.awt.image.BufferedImage
import javax.imageio.ImageIO

/** Tự sinh file mẫu để upload (avatar hợp lệ, ảnh > 1MB, file .pdf) - không cần chuẩn bị tay. */
class Files {
	static File dir() {
		File d = new File(System.getProperty('java.io.tmpdir'), 'oh_test_files')
		d.mkdirs()
		return d
	}

	/** avatar.jpg nhỏ (< 1MB) */
	static String avatar() {
		File f = new File(dir(), 'avatar.jpg')
		if (!f.exists()) {
			BufferedImage img = new BufferedImage(200, 200, BufferedImage.TYPE_INT_RGB)
			for (int x = 0; x < 200; x++) {
				for (int y = 0; y < 200; y++) {
					int rr = (x * 255).intdiv(200)
					int gg = (y * 255).intdiv(200)
					img.setRGB(x, y, (rr << 16) | (gg << 8) | 128)
				}
			}
			ImageIO.write(img, 'jpg', f)
		}
		return f.getAbsolutePath()
	}

	/** large.jpg > 1MB (ảnh nhiễu ngẫu nhiên nên nén kém) */
	static String largeJpg() {
		File f = new File(dir(), 'large.jpg')
		if (!f.exists() || f.length() < 1100000L) {
			Random r = new Random(1)
			BufferedImage img = new BufferedImage(1800, 1800, BufferedImage.TYPE_INT_RGB)
			for (int x = 0; x < 1800; x++) for (int y = 0; y < 1800; y++) img.setRGB(x, y, r.nextInt(0xFFFFFF))
			ImageIO.write(img, 'jpg', f)
		}
		return f.getAbsolutePath()
	}

	/** document.pdf (sai định dạng ảnh) */
	static String pdf() {
		File f = new File(dir(), 'document.pdf')
		if (!f.exists()) f.setText('%PDF-1.4\n% test file for upload validation\n', 'UTF-8')
		return f.getAbsolutePath()
	}
}
