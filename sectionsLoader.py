
sectionTxtTest = """I can definitely give you some ideas for an outline! Here are some sections you might want to include:

I. Introduction

Background on scaling issues with Ethereum
Overview of Layer 2 solutions
Introduce optimistic zk-rollup technology as a specific Layer 2 solution to be explored in this paper
II. Understanding Optimistic Rollups

Explanation of optimistic rollup technology
Advantages and disadvantages of optimistic rollups compared to other Layer 2 solutions
Limitations of current optimistic rollup implementations
III. Introduction to Zero-Knowledge Rollups

Explanation of zero-knowledge rollup technology
Advantages and disadvantages of zero-knowledge rollups compared to other Layer 2 solutions
Differences between optimistic and zero-knowledge rollups
IV. Optimistic ZK-Rollup Technology

Explanation of how optimistic zk-rollup technology combines the advantages of both optimistic and zero-knowledge rollups
Technical details of how it works
Potential benefits for the Ethereum network
V. Challenges and Future Directions

Limitations and challenges facing optimistic zk-rollup technology
Potential solutions or directions for further research and development
VI. Conclusion

Recap of key points
Discussion of potential impact on the Ethereum network
Possible future applications and directions for Layer 2 technology
Hope that helps get you started! Let me know if you have any other questions."""


sectionIndexs = ["\nI.","\nII.","\nIII.","\nIV.","\nV.","\nVI.","\nVII."]


def getSections(sectionTxt):
    sectionTxt = sectionTxtTest
    sections=[]
    start = 0
    for index in sectionIndexs:
        if start !=0:
            section = sectionTxt[start : sectionTxt.find(index)]
            sections.append(section)
        start = sectionTxt.find(index)
    return sections

# msg = "abc"
# msg = msg +"\n\n\n"+"efg"
# print(msg)

sections = getSections("aaa")
title = str(sections[1]).split("\n")[1]
print(title)