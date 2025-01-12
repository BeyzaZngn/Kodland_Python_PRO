import sqlite3
import random

# Sorular ve doğru/yanlış cevaplar
questions_data = [
    ('What is the primary goal of computer vision?', 'Understanding images', 'Storing data', 'Compressing files', 'Enhancing resolution'),
    ('Which algorithm is commonly used for object detection?', 'YOLO', 'SVM', 'K-means', 'Linear Regression'),
    ('What does CNN stand for?', 'Convolutional Neural Network', 'Computer Neural Network', 'Central Neural Network', 'Cognitive Neural Network'),
    ('What is the purpose of edge detection in computer vision?', 'Identify boundaries in images', 'Reduce noise', 'Increase brightness', 'Enhance sharpness'),
    ('Which dataset is commonly used for image classification tasks?', 'MNIST', 'IMDB', 'COCO', 'Imagenet'),
    ('What is the output of an image segmentation algorithm?', 'Segments of an image', 'Object labels', 'Pixel histograms', 'RGB values'),
    ('Which of these is NOT a task in computer vision?', 'Database normalization', 'Object detection', 'Face recognition', 'Image segmentation'),
    ('Which technique is used to reduce overfitting in CNNs?', 'Dropout', 'Gradient Boosting', 'Batch Normalization', 'Backpropagation'),
    ('What is a bounding box used for in computer vision?', 'Highlight objects in an image', 'Measure image sharpness', 'Segment the image', 'Analyze contrast'),
    ('What does optical flow measure?', 'Motion between frames', 'Object dimensions', 'Image contrast', 'Color intensity')
]

# Soruları rastgele dağıtılmış doğru cevaplarla veritabanına ekle
randomized_questions = []
for question, correct, wrong1, wrong2, wrong3 in questions_data:
    options = [correct, wrong1, wrong2, wrong3]
    random.shuffle(options)
    randomized_questions.append((question, options[0], options[1], options[2], options[3], correct))

# Veritabanına bağlan
conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# Eski tabloları sil
cursor.execute('DROP TABLE IF EXISTS questions')
cursor.execute('DROP TABLE IF EXISTS users')

# Sorular tablosunu oluştur
cursor.execute('''
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    correct_option TEXT NOT NULL
)
''')

# Kullanıcı tablosunu oluştur
cursor.execute('''
CREATE TABLE users (
    username TEXT PRIMARY KEY,  -- Her kullanıcı için yalnızca bir kayıt
    best_score INTEGER DEFAULT 0  -- Kullanıcının en yüksek skoru
)
''')

# Soruları ekle
cursor.executemany('''
INSERT INTO questions (question, option1, option2, option3, option4, correct_option)
VALUES (?, ?, ?, ?, ?, ?)
''', randomized_questions)

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()

print("Database setup complete!")