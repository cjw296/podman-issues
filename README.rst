.. code-block:: bash

    $ cd vcs/git/podman-issues/
    $ python3.11 -m venv .venv
    $ source .venb/bin/activate
    $ pip install -r requirements.txt
    ...

    $ python dockerpy-reproducer.py all
    $ python podmanpy-reproducer.py all
