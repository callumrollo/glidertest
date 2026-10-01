from fpdf import FPDF
from pathlib import Path
import fetchers
import plots
import matplotlib.pyplot as plt
import glob
import os
import matplotlib
matplotlib.use('agg')  # use agg backend to prevent creating plot windows during tests


def simple_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', size=12)
    pdf.cell(text="hello world")
    pdf.output("hello_world.pdf")



def _image_aspect(path: str, default: float = 0.6) -> float:
    #   Image height/width ratio (read with matplotlib); default if unreadable.
    try:
        arr = plt.imread(path)
        height, width = arr.shape[0], arr.shape[1]
        return height / width
    except Exception:  # noqa: BLE001 - sizing is best-effort, never fatal
        return default


class reportPDF(FPDF):
    def __init__(
        self):
        super().__init__(orientation="P", unit="mm", format="A4")

        self.title=None

    def h2(self, text: str) -> None:
        self.ln(2)
        self.set_font("Times", "B", 16)
        self.multi_cell(0, 9, text)
        self.ln(2)
    def section_heading(self, text: str) -> None:
        #   Level-2 heading that also registers a document section (start_section)
        #   so it lands on the contents page and PDF bookmarks. Once per section.
        self.start_section(text, level=0)
        self.h2(text)
        
    def image_fit(self, path: str, aspect: float, max_h: float) -> None:
        #   Place an image at text width but capped (and centred) at max_h height,
        #   so several plots can share a page. Breaks the page first if needed.
        w = self.epw
        h = w * aspect
        if h > max_h:
            h = max_h
            w = h / aspect
        if self.get_y() + h > self.page_break_trigger:
            self.add_page()
        #   Centre the (possibly narrowed) image within the text width.
        x = (self.w - w) / 2
        self.image(path, x=x, w=w)
        self.ln(4)


def glidertest_section(pdf, data, outdir: str) -> None:
    """
    Function is in alpha. copied from pelagos PR

    Runs plotting routines from `glidertest` and inserts them into the document.

    clone glidertest, then install with `pip install -e .` until versioning is sorted out.
    """
    from glidertest import summary_sheet as gss
    from glidertest import plots as gtplots

    print("Glidertest section is running - glidertest has been imported.")

    pdf.add_page()
    pdf.section_heading("Glidertest Plots: Basic Variables")
    if "PSAL" not in data.data_vars:
        data["PSAL"] = data["PRAC_SALINITY"]

    fig, __ = gtplots.plot_basic_vars(ds=data)
    fig_name = f"{outdir}_basic_vars.png"
    fig.savefig(fig_name)
    plt.close(fig)
    pdf.image_fit(
        fig_name,
        aspect=_image_aspect(fig_name),
        max_h=100
    )

    pdf.add_page()
    pdf.section_heading("Glidertest Plots: Up/Down bias")

    for var in ["TEMP", "CNDC", "DOXY"]:
        fig, __ = gtplots.plot_updown_bias(data, var=var)
        fig_name = f"{outdir}{var}_updown.png"
        fig.savefig(fig_name)
        plt.close(fig)
        pdf.image_fit(
            fig_name,
            aspect=_image_aspect(fig_name),
            max_h=100,
        )

    pdf.add_page()
    pdf.section_heading("Glidertest Plots: Optics assessment")

    data = data.set_coords("TIME")

    #   This step has an output - capture it (eventually) and type it in underneat the figures.
    fig, __ = gtplots.process_optics_assess(ds=data)
    fig_name = f"{outdir}_optics_assess.png"
    fig.savefig(fig_name)
    plt.close(fig)
    pdf.image_fit(
        fig_name,
        aspect=_image_aspect(fig_name),
        max_h=100
    )

    pdf.add_page()
    pdf.section_heading("Glidertest Plots: Day/night")

    #   Getting this: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
    #   Figure seems fine when saved elsewhere
    fig, __ = gtplots.plot_daynight_avg(ds=data, var="CHLA")
    fig_name = f"{outdir}_daynight_avg_sal.png"
    fig.savefig(fig_name)
    plt.close(fig)
    pdf.image_fit(
        fig_name,
        aspect=_image_aspect(fig_name),
        max_h=100
    )

    #   Summary sheet batch plots (do not export fig, ax)
    pdf.add_page()
    pdf.section_heading("Glidertest Plots: Hysteresis diagnostics")

    #   Common error: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
    if not Path(outdir).exists():
        Path(outdir).absolute().mkdir(parents=True)
    gss.create_hyst_plots(data, path=Path(outdir))
    for fig_name in sorted(glob.glob(os.path.join(outdir, "*_hyst.png"))):
        pdf.image_fit(
            fig_name,
            aspect=_image_aspect(fig_name),
            max_h=100,
        )

    pdf.add_page()
    pdf.section_heading("Glidertest Plots: Drift plots")
    #   Has a writeout - need to caputre it
    gss.create_drift_plots(data, path=outdir)
    for fig_name in sorted(glob.glob(os.path.join(outdir, "*_drift.png"))):
        pdf.image_fit(
            fig_name,
            aspect=_image_aspect(fig_name),
            max_h=100,
        )

def aaron_main():
    ds = fetchers.load_sample_dataset()
    pdf = reportPDF()
    glidertest_section(pdf, ds, outdir='report')
    pdf.output("hello_world.pdf")


if __name__ == '__main__':
    aaron_main()
