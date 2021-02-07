import os


rootDir = "../data/"
for directory, subdirectory, filenames in os.walk(rootDir):
    print(directory, subdirectory, len(filenames))




# class mail:
#     def __init__(self, _from, to, cc, bcc, subject, content):
#         self._from = _from
#         self.to = to
#         self.cc = cc
#         self.bcc = bcc
#         self.subject = subject
#         self.content = content
#
#
#
#
# _reader = EnronReader("../data/")