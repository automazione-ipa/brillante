# Programmer Kit Essentials

## Guida Uso Avanzato Git - Standard di Lavoro

### SQUASH DI x COMMIT IN UNO SOLO
 
**PREMESSA**
- Voglio che la storia del `feature-branch` sia esattamente uguale a quella di `develop`

**REGOLA**
- Non fare mai operazione di MAI su branch develop.
- I commit su develop non vanno mai toccati.

Considera gli ultimi 10 commit sul mio branch e permettimi di modificarli.
```bash
git rebase -i HEAD~10
```
Rebase sulla storia interna, fino a 10 commit prima della HEAD
Nel perimetro dei rebasati, ne voglio di più di quelli che sono nel feature-branch.

```bash
s | squash
```
Scrivo s(SQUASH) dal basso, senza toccare quelli più in alto che sono quelli che invece sono da tenere.
Quindi, salto l'ultimo che voglio tenere, lasciando "pick"

```bash
:wq | write_quit
```

Ricordiamo che in generale questa procedura serve anche per riallineare il `feature-branch` a develop.
La rebase nell'altro senso a questo punto equivale a una merge, senza conflitti (perchè avevo il feature riallineato)

Se voglio continuare questa rebase, eseguo il comando:
```bash
git rebase --continue | --abort per annullarla
```
Posso scegliere quali commenti tenere nello squash o aggiungerne uno nuovo che li riassuma, togliendo gli altri.
In alcuni casi mi fa risolvere dei conflitti.


Il feaature-branch locale ora risulta disallineato da quello remoto, poichè ho riscritto la storia locale.
Eseguo il comando:
```bash
git push -f
```
Riallineo la versione remota del FEATURE-BRANCH
 
Attenzione a non fare git push -f senza specificare il branch (soprattuto da Sandbox).
---
 
git graph -> per uscire, q



# 🐍 Anaconda Command Cheat Sheet
Concise guide in **Markdown** with the most useful Anaconda commands.

## 📋 General Commands

- **Check Conda version:**
  ```bash
  conda --version
  ```

- **Update Conda:**
  ```bash
  conda update conda
  ```

- **List all environments:**
  ```bash
  conda env list
  ```

---

## 🌱 Environment Management
- **Create a new environment:**
  ```bash
  conda create --name <env_name> python=<version>
  ```
  Example:
  ```bash
  conda create --name myenv python=3.9
  ```

- **Activate an environment:**
  ```bash
  conda activate <env_name>
  ```

- **Deactivate the current environment:**
  ```bash
  conda deactivate
  ```

- **Clone an existing environment:**
  ```bash
  conda create --name <new_env_name> --clone <existing_env_name>
  ```
  Example:
  ```bash
  conda create --name myenv-clone --clone myenv
  ```

- **Delete an environment:**
  ```bash
  conda remove --name <env_name> --all
  ```
  Example:
  ```bash
  conda remove --name myenv --all
  ```

---

## 📦 Package Management
- **Install a package in the active environment:**
  ```bash
  conda install <package_name>
  ```
  Example:
  ```bash
  conda install numpy
  ```

- **Remove a package:**
  ```bash
  conda remove <package_name>
  ```
  Example:
  ```bash
  conda remove numpy
  ```

- **Update a package:**
  ```bash
  conda update <package_name>
  ```
  Example:
  ```bash
  conda update pandas
  ```

- **List all installed packages in the current environment:**
  ```bash
  conda list
  ```

---

## 📤 Exporting & Importing Environments
- **Export an environment to a `.yml` file:**
  ```bash
  conda env export --name <env_name> > environment.yml
  ```
  Example:
  ```bash
  conda env export --name myenv > environment.yml
  ```

- **Create an environment from a `.yml` file:**
  ```bash
  conda env create --name <env_name> --file environment.yml
  ```
  Example:
  ```bash
  conda env create --name myenv-clone --file environment.yml
  ```

---

## 🛠️ Troubleshooting
- **Fix package installation issues (e.g., broken installations):**
  ```bash
  conda clean --all
  ```

- **Uninstall and reinstall a specific package to fix issues:**
  ```bash
  conda remove <package_name>
  conda install <package_name>
  ```

- **Force reinstall all packages in the environment:**
  ```bash
  conda install --revision 0
  ```

---

## 🧹 Clean Up
- **Remove unused packages and cache:**
  ```bash
  conda clean --all
  ```

---

## 🔍 Debugging Installation Issues
- **Check for corrupted installations (e.g., missing METADATA file):**
  1. Remove the faulty package manually:
     ```bash
     rm -rf <path_to_package>
     ```
  2. Reinstall the package:
     ```bash
     conda install <package_name>
     ```

- **Ignore specific Flake8 warnings/errors:**
  ```bash
  python -m flake8 --ignore E501,E722
  ```

---

Feel free to extend or customize this guide as needed. 😊

```