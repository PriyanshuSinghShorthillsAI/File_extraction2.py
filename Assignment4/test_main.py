import unittest
from unittest.mock import patch, MagicMock
from Assignment4.data_extractor.data_extractor.docx_extractor import DOCXExtractor
from Assignment4.data_extractor.data_extractor.pdf_extractor import PDFExtractor
from Assignment4.data_extractor.data_extractor.pptx_extractor import PPTXExtractor
from Assignment4.data_extractor.file_loaders.pdf_loader import PDFLoader
from Assignment4.data_extractor.file_loaders.docx_loader import DOCXLoader
from Assignment4.data_extractor.file_loaders.ppt_loader import PPTLoader
from Assignment4.data_extractor.storage.file_storage import FileStorage
from Assignment4.data_extractor.storage.sql_storage import SQLStorage

import os

class TestMain(unittest.TestCase):

    @patch('data_extractor.storage.file_storage.FileStorage')
    @patch('data_extractor.storage.sql_storage.SQLStorage')
    def test_pdf_extraction(self, MockSQLStorage, MockFileStorage):
        # Mock the file path
        file_path = "/home/shtlp_0132/Documents/Assignment_3_python-main/Assignment_3_python-main/files/sample.pdf"

        # Mock the loaders and extractors
        mock_loader = MagicMock(spec=PDFLoader)
        mock_extractor = MagicMock(spec=PDFExtractor)

        # Mock methods inside extractors
        mock_extractor.extract_text.return_value = "Sample text from PDF"
        mock_extractor.extract_images.return_value = ['image1.png', 'image2.png']
        mock_extractor.extract_urls.return_value = ['http://example.com']
        mock_extractor.extract_tables.return_value = [["Row1", "Row2"]]

        # Mock the loader and extractor instantiation
        with patch('data_extractor.file_loaders.pdf_loader.PDFLoader', return_value=mock_loader):
            with patch('data_extractor.data_extractor.pdf_extractor.PDFExtractor', return_value=mock_extractor):
                
                # Test the file extraction
                extractor = PDFExtractor(mock_loader)
                extractor.load(file_path)
                extracted_text = extractor.extract_text()
                images = extractor.extract_images()
                urls = extractor.extract_urls()
                tables = extractor.extract_tables()

                # Validate the extracted data
                self.assertEqual(extracted_text, "Sample text from PDF")
                self.assertEqual(images, ['image1.png', 'image2.png'])
                self.assertEqual(urls, ['http://example.com'])
                self.assertEqual(tables, [["Row1", "Row2"]])

                # Test file storage interactions
                mock_file_storage = MockFileStorage.return_value
                mock_file_storage.store.assert_any_call("Sample text from PDF", os.path.basename(file_path), 'text')
                mock_file_storage.store.assert_any_call(['image1.png', 'image2.png'], os.path.basename(file_path), 'image')
                mock_file_storage.store.assert_any_call(['http://example.com'], os.path.basename(file_path), 'url')
                mock_file_storage.store.assert_any_call([["Row1", "Row2"]], os.path.basename(file_path), 'table')

                # Test SQL storage interactions
                mock_sql_storage = MockSQLStorage.return_value
                mock_sql_storage.store.assert_any_call("text", "Sample text from PDF")
                mock_sql_storage.store.assert_any_call("image", ['image1.png', 'image2.png'])
                mock_sql_storage.store.assert_any_call("url", ['http://example.com'])
                mock_sql_storage.store.assert_any_call("data_table", ["Row1", "Row2"])

    @patch('data_extractor.storage.file_storage.FileStorage')
    @patch('data_extractor.storage.sql_storage.SQLStorage')
    def test_docx_extraction(self, MockSQLStorage, MockFileStorage):
        # Mock the file path
        file_path = "/home/shtlp_0132/Documents/Assignment_3_python-main/Assignment_3_python-main/files/sample.docx"

        # Mock the loaders and extractors
        mock_loader = MagicMock(spec=DOCXLoader)
        mock_extractor = MagicMock(spec=DOCXExtractor)

        # Mock methods inside extractors
        mock_extractor.extract_text.return_value = "Sample text from DOCX"
        mock_extractor.extract_images.return_value = ['image1.png', 'image2.png']
        mock_extractor.extract_urls.return_value = ['http://example.com']
        mock_extractor.extract_tables.return_value = [["Row1", "Row2"]]

        # Mock the loader and extractor instantiation
        with patch('data_extractor.file_loaders.docx_loader.DOCXLoader', return_value=mock_loader):
            with patch('data_extractor.data_extractor.docx_extractor.DOCXExtractor', return_value=mock_extractor):
                
                # Test the file extraction
                extractor = DOCXExtractor(mock_loader)
                extractor.load(file_path)
                extracted_text = extractor.extract_text()
                images = extractor.extract_images()
                urls = extractor.extract_urls()
                tables = extractor.extract_tables()

                # Validate the extracted data
                self.assertEqual(extracted_text, "Sample text from DOCX")
                self.assertEqual(images, ['image1.png', 'image2.png'])
                self.assertEqual(urls, ['http://example.com'])
                self.assertEqual(tables, [["Row1", "Row2"]])

                # Test file storage interactions
                mock_file_storage = MockFileStorage.return_value
                mock_file_storage.store.assert_any_call("Sample text from DOCX", os.path.basename(file_path), 'text')
                mock_file_storage.store.assert_any_call(['image1.png', 'image2.png'], os.path.basename(file_path), 'image')
                mock_file_storage.store.assert_any_call(['http://example.com'], os.path.basename(file_path), 'url')
                mock_file_storage.store.assert_any_call([["Row1", "Row2"]], os.path.basename(file_path), 'table')

                # Test SQL storage interactions
                mock_sql_storage = MockSQLStorage.return_value
                mock_sql_storage.store.assert_any_call("text", "Sample text from DOCX")
                mock_sql_storage.store.assert_any_call("image", ['image1.png', 'image2.png'])
                mock_sql_storage.store.assert_any_call("url", ['http://example.com'])
                mock_sql_storage.store.assert_any_call("data_table", ["Row1", "Row2"])


if __name__ == '__main__':
    unittest.main()
