import yaml

with open('root.yml') as fp:
    x = yaml.load(fp)
    print(x)
