import click
import pandas as pd
import fitz
import os


@click.command()
@click.argument('fname')
def load_file(fname):
    check_file = os.path.isfile(fname)
    if check_file == False:
        click.echo(f"Invalid input. Please use a valid file.")
    else:
        try:
            text_list = get_text(fname)
            df = create_csv()
            df = fill_csv(df, text_list)
            write_csv(df, fname)
            click.echo("Text successfully extracted and written to same path!")
        except ValueError:
            print("Extraction failed! Please use the correct file template.")


def get_text(fname):
    """Get the text from the PDF file.

    Args:
        fname (str): PDF file name

    Returns:
        list: Extracted PDF text
    """
    # Open the PDF file
    doc = fitz.open(fname)

    # Extract all text
    text_list = []
    i = 0
    for page in doc:
        text = page.get_text()
        cur_list = text.splitlines()
        i += 1
        text_list.extend(cur_list[:-1])
    return text_list


def create_csv():
    """Create data frame with the selected columns.

    Returns:
        obj: Empty data frame for the data
    """
    df = pd.DataFrame(
        columns=[
            "Main Billing/Entity",
            "Client ID",
            "Addressee",
            "Salutation",
            "Address",
            "Email",
            "Filter",
            "Partner Name",
            "Category",
            "Turnover",
            "Cost",
            "Associates",
        ]
    )
    return df


def fill_csv(df, text_list):
    """Fill the data frame with clean PDF data

    Args:
        df (obj): Empty data frame
        text_list (list): Raw PDF data

    Returns:
        obj: Filled data frame with the PDF data
    """
    row = -1
    text_len = len(text_list)
    # Assigning data of next lines based on the label
    for i, line in enumerate(text_list):
        if i + 1 < text_len:
            next = text_list[i + 1]
            if "Main Billing/Entity:" in line:
                row += 1
                df.at[row, "Main Billing/Entity"] = next
            elif "Client ID:" in line:
                df.at[row, "Client ID"] = next
            elif "Addressee:" in line:
                df.at[row, "Addressee"] = next
            elif "Salutation:" in line:
                df.at[row, "Salutation"] = next
            elif "Address:" in line:
                df.at[row, "Address"] = next
            elif "Email:" in line:
                df.at[row, "Email"] = next
            elif "Filter:" in line:
                df.at[row, "Filter"] = next
            elif "Partner Name:" in line:
                df.at[row, "Partner Name"] = next
            elif "Category:" in line:
                if "$" in next:
                    idx = next.find("$")
                    df.at[row, "Category"] = next[:idx]
                    df.at[row, "Turnover"] = next[idx:]
                else:
                    df.at[row, "Category"] = next
                    df.at[row, "Turnover"] = text_list[i + 2]
            elif "Cost:" in line:
                df.at[row, "Cost"] = next
            elif "Associates:" in line:
                assoc = add_associates(i, text_len, text_list)
                df.at[row, "Associates"] = assoc
    return df


def add_associates(i, text_len, text_list):
    """Merge and clean associate lines

    Args:
        i (int): Current associate text index in text list
        text_len (int): Full text list length
        text_list (list): Full text
    Returns:
        assoc: Full clean associate value
    """
    assoc = ""
    end_idx = text_len
    cur_i = i
    try:
        end_idx = text_list[i:].index("Main Billing/Entity:") + i
    except ValueError:
        pass
    
    # Removing list numbers if exist and merge text
    while cur_i + 1 < end_idx:
        if text_list[cur_i + 1][0].isnumeric():
            idx = text_list[cur_i + 1].find(".")
            item = text_list[cur_i + 1][idx + 2 :]
            if cur_i + 2 != end_idx:
                item += "\n"
            assoc += item
            cur_i += 1
        else:
            item = text_list[cur_i + 1]
            assoc += item
            cur_i += 1
    return assoc


def write_csv(df, fname):
    """Write filled data frame as csv file in the same file path.

    Args:
        df (obj): Filled data
        fname (str): file name

    Returns:
        None
    """
    df.to_csv(f"{fname[:-4]}.csv", index=False)
    return None


if __name__ == "__main__":
    load_file()
