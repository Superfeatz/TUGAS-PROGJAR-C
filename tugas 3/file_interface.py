
import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        # Pastikan direktori 'files' ada
        if not os.path.exists('files/'):
            os.makedirs('files/')
        os.chdir('files/')

    def list(self, params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK', data=filelist)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def get(self, params=[]):
        try:
            if not params:
                return dict(status='ERROR', data='Nama file tidak boleh kosong')
            
            filename = params[0]
            if (filename == ''):
                return dict(status='ERROR', data='Nama file tidak boleh kosong')
                
            # Cek apakah file ada
            if not os.path.exists(filename):
                return dict(status='ERROR', data=f'File {filename} tidak ditemukan')
                
            fp = open(f"{filename}", 'rb')
            isifile = base64.b64encode(fp.read()).decode()
            fp.close()
            return dict(status='OK', data_namafile=filename, data_file=isifile)
        except Exception as e:
            return dict(status='ERROR', data=str(e))
    
    def upload(self, params=[]):
        try:
            if len(params) < 2:
                return dict(status='ERROR', data='Parameter kurang')
            filename = params[0]
            isifile = base64.b64decode(params[1])
            with open(filename, 'wb') as fp:
                fp.write(isifile)
            return dict(status='OK', data=f'File {filename} berhasil diupload')
        except Exception as e:
            return dict(status='ERROR', data=str(e))
    
    def delete(self, params=[]):
        try:
            if len(params) < 1:
                return dict(status='ERROR', data='Parameter kurang')
            filename = params[0]
            if os.path.exists(filename):
                os.remove(filename)
                return dict(status='OK', data=f'File {filename} berhasil dihapus')
            else:
                return dict(status='ERROR', data=f'File {filename} tidak ditemukan')
        except Exception as e:
            return dict(status='ERROR', data=str(e))


if __name__=='__main__':
    f = FileInterface()
    print(f.list())
    # Test fungsi get hanya jika file ada
    if os.path.exists('pokijan.jpg'):
        print(f.get(['pokijan.jpg']))
    else:
        print("File pokijan.jpg tidak ada untuk testing")
