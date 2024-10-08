.. _code_style:

Code Style
==========

To standardize the code included in this post-processing repository, it is run through automatic formatters and linters.

.. warning::

    For software quality assurance, formatting and linting checks are automatically run on all Pull Requests (and commits) to the Main branch of the repository.
    When developing this code and submitting a Pull Request, please run all the formatters and linters locally to ensure the code is properly formatted.
    If the code is not properly formatted, the Pull Request checks will fail.

Python Code
-----------

`black <https://pypi.org/project/black/>`_
******************************************

``black`` is an automatic formatting tool that will reformat any Python file on which it is called.
The tool is available on PyPI and can be installed using PIP:

.. prompt:: bash

    pip3 install black

For this repository, ``black`` is run using its default configuration, apart from the line length option that is set to 120 characters using the ``-l`` flag:

.. prompt:: bash

    black -l 120 .

This command should be executed in the root directory and should apply to all of the Python code in the repository.

.. note::

    If there is a scenario in which ``black`` formatting should not be applied to a block of code, the block can be wrapped in the ``# fmt: off`` and ``# fmt: on`` directives.
    This block will not be affected by ``black``.


`flake8 <https://pypi.org/project/flake8/>`_
********************************************

``flake8`` is a linting tool that will identify issues in Python code and write them to the terminal without modifying the file.
``flake8`` is often more strict than ``black`` and helps ensure that all the Python code within this repository is up to the correct standard.
The tool is available on PyPI and can be installed using PIP:

.. prompt:: bash

    pip3 install flake8

``flake8`` can be run with a configuration file that specifies a variety of options.
The configuration file for this repository is included in the root directory with the following configuration options:

.. literalinclude:: ../../.flake8

To run ``flake8``, navigate to the root directory and execute the following command:

.. prompt:: bash

    flake8 .

This command outputs all of the linting errors to the terminal.

.. note::

    If there is a scenario in which ``flake8`` should ignore a specific linting error, the error tag can be added using the inline comment ``# NOQA: <error tag>``.
    If the error is general and must be repeatedly ignored, the tag to be ignored can be added to the ``flake8`` configuration file in root directory.
