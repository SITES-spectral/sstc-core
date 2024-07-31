## How to Update Individual Files

To update individual files using the `update_catalog_backup` function, you need to provide the following arguments:

1. **The directory containing the original files**: This is the directory where the files you want to check are located.
2. **The name of the file you want to check**: This is the specific file you want to compare and potentially update in the backup directory.
3. **The directory containing the backup files**: This is where the backup files are stored, and where the updated files will be copied if changes are detected.

### Example Command

```bash
update_catalog_backup "/home/aurora02/data/SITES/Spectral/data/catalog/abisko/" "abisko_catalog.db" "/home/aurora02/data/SITES/Spectral/code/pycode/SSTC/sstc-catalog/src/sstc_catalog/databases/"
```

In this example:
- The original file directory is `/home/aurora02/data/SITES/Spectral/data/catalog/abisko/`.
- The file to check and update is `abisko_catalog.db`.
- The backup directory is `/home/aurora02/data/SITES/Spectral/code/pycode/SSTC/sstc-catalog/src/sstc_catalog/databases/`.

### Sourcing the Script

The source bash script is located at:

`/home/aurora02/data/SITES/Spectral/code/bash_scripts/backup_update.sh`

This script has been sourced by adding it to the `.bashrc` of the user, ensuring it is available in all terminal sessions. You can also source the script manually in your terminal by running:

```bash
source /home/aurora02/data/SITES/Spectral/code/bash_scripts/backup_update.sh
```

This will load the function into your current shell session, allowing you to use the `update_catalog_backup` function as needed.

## How to Update Multiple Files

To update multiple files at once, you can call the bash script located at `/home/aurora02/data/SITES/Spectral/code/bash_scripts/sites_spectral_update_catalogs.sh`. This script should contain individual calls to the `update_catalog_backup` function for each station catalog you wish to update.

### Example Script Structure

The `sites_spectral_update_catalogs.sh` script should include lines similar to the following for each file you want to update:

```bash
#!/bin/bash

# Call the update_catalog_backup function for each station catalog

# Abisko station
update_catalog_backup "/home/aurora02/data/SITES/Spectral/data/catalog/abisko/" "abisko_catalog.db" "/home/aurora02/data/SITES/Spectral/code/pycode/SSTC/sstc-catalog/src/sstc_catalog/databases/"

# Another station
update_catalog_backup "/path/to/original/files/station2/" "station2_catalog.db" "/path/to/backup/files/"

# Add more calls as needed...
```

### Running the Script

To run the script and update all specified files, navigate to the directory containing your script and execute it:

```bash
cd /home/aurora02/data/SITES/Spectral/code/bash_scripts/
./sites_spectral_update_catalogs.sh
```

Alternatively, if you're already in a different directory and want to run the script, you can execute it with the full path:

```bash
/home/aurora02/data/SITES/Spectral/code/bash_scripts/sites_spectral_update_catalogs.sh
```

### Making the Script Executable

Ensure the script has execute permissions. If not, you can make it executable with the following command:

```bash
chmod +x /home/aurora02/data/SITES/Spectral/code/bash_scripts/sites_spectral_update_catalogs.sh
```

### Summary

- **Individual updates** can be done using the `update_catalog_backup` function with specific arguments.
- **Batch updates** can be managed by calling the `sites_spectral_update_catalogs.sh` script, which contains multiple function calls for different station catalogs.