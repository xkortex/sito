if __name__ == "__main__":
    from sito import __version__ as sito_version

    print("{: <10} {: >30}".format("sito", sito_version))
    try:
        from sito.sci import __version__ as sito_sci_version
        print("{: <10} {: >30}".format("sito.sci", sito_sci_version))
    except ImportError:
        pass
