import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSpinBox
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor


class GridBotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Row-Priority Search with Adjacent Recovery")
        self.resize(1000, 520)

        self.grid_size = 4
        self.target = None

        # Search state
        self.search_rows = []
        self.current_row_index = 0
        self.current_col = 0
        self.dir = 1

        self.init_ui()
        self.init_timer()

    # ---------------- UI ---------------- #

    def init_ui(self):
        main = QVBoxLayout(self)

        title = QLabel("🤖 Database-Guided Search with Adjacent Row Recovery")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        main.addWidget(title)

        top = QHBoxLayout()
        self.size_spin = QSpinBox()
        self.size_spin.setRange(2, 10)
        self.size_spin.setValue(self.grid_size)
        self.size_spin.setPrefix("Grid: ")

        self.target_spin = QSpinBox()
        self.target_spin.setRange(1, 999)
        self.target_spin.setPrefix("Target: ")

        apply_btn = QPushButton("Apply Size")
        apply_btn.clicked.connect(self.apply_size)

        top.addWidget(self.size_spin)
        top.addWidget(self.target_spin)
        top.addWidget(apply_btn)
        main.addLayout(top)

        self.grids = QHBoxLayout()
        main.addLayout(self.grids)

        controls = QHBoxLayout()
        start = QPushButton("▶ Start")
        rand = QPushButton("🎲 Random World")
        reset = QPushButton("⟲ Reset")

        start.clicked.connect(self.start)
        rand.clicked.connect(self.randomize_world)
        reset.clicked.connect(self.reset)

        for b in [start, rand, reset]:
            controls.addWidget(b)

        main.addLayout(controls)

        self.build_grids()

    # ---------------- Grids ---------------- #

    def build_grids(self):
        while self.grids.count():
            w = self.grids.takeAt(0).widget()
            if w:
                w.deleteLater()

        self.db = self.make_grid("Database")
        self.world = self.make_grid("World")
        self.cache = self.make_grid("New Data (Cache)")

        self.grids.addWidget(self.db["container"])
        self.grids.addWidget(self.world["container"])
        self.grids.addWidget(self.cache["container"])

        self.populate_database()
        self.copy_db_to_world()
        self.clear_cache()
        self.adjust_cells()

    def make_grid(self, title):
        cont = QWidget()
        v = QVBoxLayout(cont)
        v.addWidget(QLabel(title))
        table = QTableWidget(self.grid_size, self.grid_size)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        table.setStyleSheet("font-size:16px;")
        v.addWidget(table)
        return {"container": cont, "table": table}

    # ---------------- Data ---------------- #

    def populate_database(self):
        n = 1
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                self.db["table"].setItem(r, c, QTableWidgetItem(str(n)))
                n += 1

    def copy_db_to_world(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                self.world["table"].setItem(
                    r, c,
                    QTableWidgetItem(self.db["table"].item(r, c).text())
                )

    def randomize_world(self):
        vals = [
            self.world["table"].item(r, c).text()
            for r in range(self.grid_size)
            for c in range(self.grid_size)
        ]
        random.shuffle(vals)
        i = 0
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                self.world["table"].setItem(
                    r, c, QTableWidgetItem(vals[i])
                )
                i += 1

    # ---------------- Algorithm ---------------- #

    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)

    def start(self):
        self.reset()
        self.target = self.target_spin.value()

        # --- Database row lookup ---
        base_row = None
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if int(self.db["table"].item(r, c).text()) == self.target:
                    base_row = r
                    break

        if base_row is None:
            return

        # --- Build adjacent search order ---
        self.search_rows = [base_row]
        for d in range(1, self.grid_size):
            if base_row - d >= 0:
                self.search_rows.append(base_row - d)
            if base_row + d < self.grid_size:
                self.search_rows.append(base_row + d)

        self.current_row_index = 0
        self.current_col = 0
        self.dir = 1

        self.timer.start(600)

    def step(self):
        if self.current_row_index >= len(self.search_rows):
            self.timer.stop()
            return

        row = self.search_rows[self.current_row_index]
        col = self.current_col
        world_val = int(self.world["table"].item(row, col).text())

        item = QTableWidgetItem(str(world_val))

        if world_val == self.target:
            item.setBackground(QColor("lightgreen"))
            self.cache["table"].setItem(row, col, item)
            self.timer.stop()
            return
        else:
            item.setBackground(QColor("red"))
            self.cache["table"].setItem(row, col, item)

        # Move horizontally
        nc = col + self.dir
        if nc < 0 or nc >= self.grid_size:
            self.dir *= -1
            # Row finished → go to next adjacent row
            self.current_row_index += 1
            self.current_col = 0
        else:
            self.current_col = nc

    # ---------------- Utils ---------------- #

    def reset(self):
        self.timer.stop()
        self.clear_cache()

    def clear_cache(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                self.cache["table"].setItem(r, c, QTableWidgetItem(""))

    def apply_size(self):
        self.grid_size = self.size_spin.value()
        self.build_grids()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.adjust_cells()

    def adjust_cells(self):
        size = max(30, self.width() // (3 * self.grid_size))
        for g in [self.db, self.world, self.cache]:
            t = g["table"]
            for i in range(self.grid_size):
                t.setRowHeight(i, size)
                t.setColumnWidth(i, size)


# ---------------- Main ---------------- #

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GridBotGUI()
    w.show()
    sys.exit(app.exec())
