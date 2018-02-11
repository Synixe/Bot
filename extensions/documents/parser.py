import re

class Parser:
    def __init__(self, data):
        self.data = data
        self.document = False
        self.list = False
        self.section = -1
        self.subsection = -1
        self.subsubsection = -1
        self.item = -1
        self.sections = []
        self.references = {}
        for l in self.data.split("\n"):
            l = l.replace("\t", "").replace("\\&", "&")
            if not self.document:
                if l == "\\begin{document}":
                    self.document = True
            elif not self.list:
                if l.startswith("\\section"):
                    self.section += 1
                    self.subsection = -1
                    self.sections.append({"name": l.split("{", 1)[1].split("}")[0], "subsections": [], "text": "", "items": []})
                elif l.startswith("\\subsection"):
                    self.subsection += 1
                    self.subsubsection = -1
                    self.sections[self.section]["subsections"].append({"name": l.split("{", 1)[1].split("}")[0], "subsubsections": [], "text": "", "items": []})
                elif l.startswith("\\subsubsection"):
                    self.subsubsection += 1
                    self.sections[self.section]["subsections"][self.subsection]["subsubsections"].append({"name": l.split("{", 1)[1].split("}")[0], "text": "", "items": []})
                elif l.startswith("\\begin{enumerate}"):
                    self.list = True
                    self.item = -1
                elif not l.startswith("\\") and self.section != -1:
                    if self.subsection == -1:
                        self.sections[self.section]["text"] += l + "\n"
                    elif self.subsubsection == -1:
                        self.sections[self.section]["subsections"][self.subsection]["text"] += l + "\n\n"
                    else:
                        self.sections[self.section]["subsections"][self.subsection]["subsubsections"][self.subsubsection]["text"] += l + "\n\n"
                if "\\label" in l:
                    ref = l.split("\\label{")[1].split("}")[0]
                    if self.subsubsection != -1:
                        self.references[ref] = "{}.{}.{}".format(self.section + 1, self.subsection + 1, self.subsubsection + 1)
                    elif self.subsection != -1:
                        self.references[ref] = "{}.{}".format(self.section + 1, self.subsection + 1)
                    else:
                        self.references[ref] = "{}".format(self.section + 1)
            elif self.list:
                if l.startswith("\\item"):
                    self.item += 1
                    if self.subsection == -1:
                        self.sections[self.section]["items"].append(l.replace("\\item ", ""))
                    elif self.subsubsection == -1:
                        self.sections[self.section]["subsections"][self.subsection]["items"].append(l.replace("\\item ", ""))
                    else:
                        self.sections[self.section]["subsections"][self.subsection]["subsubsections"][self.subsubsection]["items"].append(l.replace("\\item ", ""))
                elif l.startswith("\\end"):
                    self.list = False

    def processRef(self, text):
        return re.sub(r'\\ref{(.+?)}', lambda match: self.references[match.group(1)], text)

    def getByID(self, tag):
        sections = tag.split(".")
        if len(sections) == 1:
            return self.sections[int(tag) - 1]
        elif len(sections) == 2:
            try:
                return self.sections[int(sections[0]) - 1]["subsections"][int(sections[1]) - 1]
            except:
                return self.sections[int(sections[0]) - 1]["items"][int(sections[1]) - 1]
        elif len(sections) == 3:
            try:
                return self.sections[int(sections[0]) - 1]["subsections"][int(sections[1]) - 1]["items"][int(sections[2]) - 1]
            except:
                return self.sections[int(sections[0]) - 1]["subsections"][int(sections[1]) - 1]["subsubsections"][int(sections[2]) - 1]
        elif len(sections) == 4:
            return self.sections[int(sections[0]) - 1]["subsections"][int(sections[1]) - 1]["subsubsections"][int(sections[2]) - 1]["items"][int(sections[3]) - 1]
