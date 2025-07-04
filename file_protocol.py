import json
import logging
import shlex

from file_interface import FileInterface

"""
* class FileProtocol bertugas untuk memproses 
data yang masuk, dan menerjemahkannya apakah sesuai dengan
protokol/aturan yang dibuat

* data yang masuk dari client adalah dalam bentuk bytes yang 
pada akhirnya akan diproses dalam bentuk string

* class FileProtocol akan memproses data yang masuk dalam bentuk
string
"""
class FileProtocol:
    def __init__(self):
        self.file = FileInterface()
        
    def proses_string(self, string_datamasuk=''):
        logging.warning(f"string diproses: {string_datamasuk}")
        try:
            # Gunakan shlex.split untuk memecah string, menghormati tanda kutip
            c = shlex.split(string_datamasuk)
            if not c:
                return json.dumps(dict(status='ERROR', data='request kosong'))
            
            c_request = c[0].strip().lower()
            logging.warning(f"memproses request: {c_request}")
            
            # Validasi request yang didukung
            if c_request not in ['list', 'get', 'upload', 'delete']:
                return json.dumps(dict(status='ERROR', data=f'request {c_request} tidak dikenali'))
            
            params = c[1:]
            cl = getattr(self.file, c_request)(params)
            return json.dumps(cl)
        except Exception as e:
            logging.error(f"Error memproses request: {str(e)}")
            return json.dumps(dict(status='ERROR', data=f'Error: {str(e)}'))


if __name__=='__main__':
    #contoh pemakaian
    fp = FileProtocol()
    print(fp.proses_string("LIST"))
    print(fp.proses_string("GET pokijan.jpg"))
