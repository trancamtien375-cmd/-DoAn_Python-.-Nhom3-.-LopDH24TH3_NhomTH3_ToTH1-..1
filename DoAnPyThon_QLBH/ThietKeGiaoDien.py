import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import random
import os

# ====================== KẾT NỐI MySQL ======================
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="QuanLyBanHang"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi CSDL", f"Không kết nối được: {err}")
        return None
# ====================== CĂN GIỮA CỬA SỔ ======================
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

# ====================== IN HÓA ĐƠN TXT ======================
def in_hoa_don_txt(ma_hd, ngay_lap, ma_nv, ten_nv, ma_kh, ten_kh, cart, tong_tien):
    # Tạo thư mục lưu hóa đơn nếu chưa có
    folder = "HoaDon"
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(folder, f"{ma_hd}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write("        HÓA ĐƠN BÁN HÀNG\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Mã HD: {ma_hd}\n")
        f.write(f"Ngày lập: {ngay_lap}\n")
        f.write(f"Nhân viên: {ten_nv} ({ma_nv})\n")
        f.write(f"Khách hàng: {ten_kh}")
        if ma_kh and ma_kh != "Khách lẻ":
            f.write(f" (Mã KH: {ma_kh})")
        f.write("\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'STT':<4} {'Tên SP':<25} {'SL':<4} {'Đơn giá':<12} {'Thành tiền':<12}\n")
        f.write("-" * 50 + "\n")

        for i, item in enumerate(cart, 1):
            f.write(f"{i:<4} {item['ten'][:24]:<25} {item['sl']:<4} {item['gia']:>10,.0f}  {item['sub']:>12,.0f}\n")

        f.write("-" * 50 + "\n")
        f.write(f"{'TỔNG TIỀN:':>38} {tong_tien:>12,.0f} VND\n")
        f.write("=" * 50 + "\n")
        f.write("        CẢM ƠN QUÝ KHÁCH - HẸN GẶP LẠI!\n")
        f.write("=" * 50 + "\n")

    # Mở file tự động
    os.startfile(file_path)  # Windows
    # Nếu dùng macOS: os.system(f"open {file_path}")
    # Nếu dùng Linux: os.system(f"xdg-open {file_path}")

    messagebox.showinfo("IN HÓA ĐƠN", f"Đã in hóa đơn!\nFile: {file_path}")

# ====================== FORM ĐĂNG NHẬP ======================
def create_login_window():
    global login_window, entry_user, entry_pass

    login_window = tk.Tk()
    login_window.title("Đăng Nhập - POS System")
    login_window.configure(bg="#ffffff")
    login_window.resizable(False, False)
    center_window(login_window, 500, 400)

    tk.Label(login_window, text="ĐĂNG NHẬP", font=("Time New Roman", 28, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=(50, 25))
    form_frame = tk.Frame(login_window, bg="#ffffff")
    form_frame.pack(pady=(0, 20))

    tk.Label(form_frame, text="Tên đăng nhập", font=("Time New Roman", 12), bg="#ffffff", fg="#34495e").pack(anchor="w", padx=80, pady=(0, 5))
    entry_user = tk.Entry(form_frame, font=("Time New Roman", 13), width=28, relief="solid", bd=1, highlightthickness=2, highlightcolor="#3498db")
    entry_user.pack(pady=(0, 15), ipady=10, padx=80)
    entry_user.focus()

    tk.Label(form_frame, text="Mật khẩu", font=("Time New Roman", 12), bg="#ffffff", fg="#34495e").pack(anchor="w", padx=80, pady=(0, 5))
    entry_pass = tk.Entry(form_frame, font=("Time New Roman", 13), width=28, show="*", relief="solid", bd=1, highlightthickness=2, highlightcolor="#3498db")
    entry_pass.pack(pady=(0, 35), ipady=10, padx=80)

    def check_login():
        username = entry_user.get().strip()
        password = entry_pass.get()
        if not username or not password:
            messagebox.showwarning("Thiếu", "Vui lòng nhập đầy đủ!")
            return
        if username == "NYCT" and password == "782823":
            messagebox.showinfo("Thành công", f"Chào {username}!")
            login_window.destroy()
            open_main_window()
        else:
            messagebox.showerror("Lỗi", "Sai thông tin đăng nhập!")

    btn_login = tk.Button(login_window, text="ĐĂNG NHẬP", font=("Time New Roman", 14, "bold"), bg="#27ae60", fg="white", width=25, height=2, command=check_login)
    btn_login.pack(pady=10)
    btn_login.bind("<Enter>", lambda e: btn_login.config(bg="#219653"))
    btn_login.bind("<Leave>", lambda e: btn_login.config(bg="#27ae60"))

    entry_pass.bind("<Return>", lambda e: check_login())
    entry_user.bind("<Return>", lambda e: entry_pass.focus())

    tk.Label(login_window, text="© 2025 Hệ thống quản lý bán hàng", font=("Time New Roman", 9), bg="#ffffff", fg="#95a5a6").pack(side="bottom", pady=20)
    login_window.maiHàng", ["ma_kh", "ten_kh", "dia_chi", "sdt_kh"], ["Mã KH", "Tên KH", "Địa chỉ", "SĐT"]), **btn_style).pack(pady=10)

    main.mainloop()

# ====================== CRUD CHUNG ======================
def open_crud_window(prev, table, cols, labels):
    prev.destroy()
    win = tk.Tk()
    win.title(f"QUẢN LÝ {table.upper()}")
    win.geometry("1300x750")
    center_window(win, 1300, 750)
    win.configure(bg="#f0f2f5")

    tk.Label(win, text=f"QUẢN LÝ {table.upper()}", font=("Time New Roman", 24, "bold"), bg="#f0f2f5", fg="#2c3e50").pack(pady=15)

    search_frame = tk.Frame(win, bg="#f0f2f5")
    search_frame.pack(pady=5)
    tk.Label(search_frame, text="Tìm kiếm:", bg="#f0f2f5").pack(side="left", padx=5)
    entry_search = tk.Entry(search_frame, width=40)
    entry_search.pack(side="left", padx=5)
    tk.Button(search_frame, text="Tìm", bg="#3498db", fg="white", command=lambda: load_data(entry_search.get().strip())).pack(side="left", padx=5)
    tk.Button(search_frame, text="Tất cả", bg="#95a5a6", fg="white", command=lambda: [entry_search.delete(0, tk.END), load_data()]).pack(side="left", padx=5)

    form = tk.LabelFrame(win, text=" THÔNG TIN ", font=("Time New Roman", 14, "bold"), bg="white", bd=2)
    form.pack(pady=10, padx=20, fill="x")

    entries = {}
    for i, label in enumerate(labels):
        tk.Label(form, text=label + ":", bg="white").grid(row=i//2, column=(i%2)*2, padx=10, pady=8, sticky="w")

        if label in ["Mã NV", "Mã SP", "Mã KH"]:
            e = tk.Entry(form, width=15, state="readonly")
            e.grid(row=i//2, column=(i%2)*2+1, padx=10, pady=8)
            entries[label] = e
        elif label == "Giới tính":
            var = tk.StringVar(value="Nam")
            tk.Radiobutton(form, text="Nam", variable=var, value="Nam", bg="white").grid(row=i//2, column=(i%2)*2+1, sticky="w")
            tk.Radiobutton(form, text="Nữ", variable=var, value="Nữ", bg="white").grid(row=i//2, column=(i%2)*2+1, padx=60, sticky="w")
            entries[label] = var
        elif label == "Chức vụ":
            e = ttk.Combobox(form, values=["Quản Lý", "Nhân Viên Bán Hàng", "Kế Toán"], state="readonly", width=27)
            e.set("Nhân Viên Bán Hàng")
            e.grid(row=i//2, column=(i%2)*2+1, padx=10, pady=8)
            entries[label] = e
        elif label == "Tồn kho":
            e = tk.Entry(form, width=15)
            e.insert(0, "0")
            e.grid(row=i//2, column=(i%2)*2+1, padx=10, pady=8)
            entries[label] = e
        else:
            width = 40 if "tên" in label.lower() or "địa chỉ" in label.lower() else 20
            e = tk.Entry(form, width=width)
            e.grid(row=i//2, column=(i%2)*2+1, padx=10, pady=8)
            entries[label] = e

    tree = ttk.Treeview(win, columns=cols, show="headings", height=15)
    for col in cols:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=150, anchor="center")
    tree.pack(pady=10, padx=20, fill="both", expand=True)

    def load_data(keyword=""):
        for i in tree.get_children(): tree.delete(i)
        conn = connect_db()
        if not conn: return
        cur = conn.cursor()
        try:
            if keyword:
                if table == "SanPham":
                    cur.execute(f"SELECT * FROM {table} WHERE ten_sp LIKE %s OR ma_sp LIKE %s", (f"%{keyword}%", f"%{keyword}%"))
                elif table == "KhachHang":
                    cur.execute(f"SELECT * FROM {table} WHERE ten_kh LIKE %s OR sdt_kh LIKE %s", (f"%{keyword}%", f"%{keyword}%"))
                else:
                    cur.execute(f"SELECT * FROM {table} WHERE ten_nv LIKE %s OR ma_nv LIKE %s", (f"%{keyword}%", f"%{keyword}%"))
            else:
                cur.execute(f"SELECT * FROM {table}")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)
        finally:
            cur.close()
            conn.close()

    def generate_id(prefix, col):
        conn = connect_db()
        if not conn: return f"{prefix}0001"
        cur = conn.cursor()
        try:
            cur.execute(f"SELECT {col} FROM {table} ORDER BY {col} DESC LIMIT 1")
            last = cur.fetchone()
        finally:
            cur.close()
            conn.close()
        if last and last[0] and str(last[0]).startswith(prefix):
            try:
                num = int(str(last[0])[len(prefix):]) + 1
                return f"{prefix}{num:04d}"
            except:
                pass
        return f"{prefix}0001"

    def them():
        values = []
        insert_cols = []
        ma = None

        if table == "NhanVien":
            ten = entries["Họ tên"].get().strip()
            gt = entries["Giới tính"].get()
            dc = entries["Địa chỉ"].get().strip()  # SỬA: "Địa chỉ" thay vì "Địa chi"
            sdt = entries["SĐT"].get().strip()
            cv = entries["Chức vụ"].get()
            if not ten:
                messagebox.showwarning("Lỗi", "Vui lòng nhập họ tên!")
                return
            ma = generate_id("NV", "ma_nv")
            values = [ma, ten, gt, dc or None, sdt or None, cv]
            insert_cols = ["ma_nv", "ten_nv", "gioitinh", "dia_chi", "sdt", "chuc_vu"]  # SỬA: gioi_tinh → gioitinh
            entries["Mã NV"].config(state="normal")
            entries["Mã NV"].delete(0, tk.END)
            entries["Mã NV"].insert(0, ma)
            entries["Mã NV"].config(state="readonly")

        elif table == "KhachHang":
            ten = entries["Tên KH"].get().strip()
            dia_chi = entries["Địa chỉ"].get().strip()
            sdt = entries["SĐT"].get().strip()
            if not ten:
                messagebox.showwarning("Lỗi", "Vui lòng nhập tên khách hàng!")
                return
            ma = generate_id("KH", "ma_kh")
            values = [ma, ten, dia_chi or None, sdt or None]
            insert_cols = ["ma_kh", "ten_kh", "dia_chi", "sdt"]  # SỬA: sdt_kh
            entries["Mã KH"].config(state="normal")
            entries["Mã KH"].delete(0, tk.END)
            entries["Mã KH"].insert(0, ma)
            entries["Mã KH"].config(state="readonly")

        elif table == "SanPham":
            ten = entries["Tên SP"].get().strip()
            loai = entries["Loại"].get().strip()
            mo_ta = entries["Mô tả"].get().strip()
            gia = entries["Giá"].get().strip()
            ton = entries["Tồn kho"].get().strip() or "0"
            if not ten:
                messagebox.showwarning("Lỗi", "Nhập tên sản phẩm!")
                return
            try:
                gia_float = float(gia.replace(",", ""))
                ton_int = int(ton)
            except:
                messagebox.showwarning("Lỗi", "Giá và tồn kho phải là số!")
                return
            ma = generate_id("SP", "ma_sp")
            values = [ma, ten, loai or None, mo_ta or None, gia_float, ton_int]
            insert_cols = ["ma_sp", "ten_sp", "loai_sp", "mo_ta", "gia", "so_luong_ton"]
            entries["Mã SP"].config(state="normal")
            entries["Mã SP"].delete(0, tk.END)
            entries["Mã SP"].insert(0, ma)
            entries["Mã SP"].config(state="readonly")

        conn = connect_db()
        if not conn:
            return
        cur = conn.cursor()
        placeholders = ",".join(["%s"] * len(values))
        try:
            cur.execute(f"INSERT INTO {table} ({','.join(insert_cols)}) VALUES ({placeholders})", values)
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã thêm: {ma}")
            load_data()        # Tải lại dữ liệu
            clear_form()       # Xóa form
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi CSDL", f"Không thêm được: {e}\nChi tiết: {e.msg}")
        finally:
            cur.close()
            conn.close()
            load_data()
            clear_form()

    def sua():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Lỗi", "Chọn dòng để sửa!")
            return
        item = tree.item(selected[0])['values']
        ma = item[0]
        values = []
        update_cols = []
        for label in labels:
            if label in ["Mã NV", "Mã SP", "Mã KH"]: continue
            val = entries[label].get() if hasattr(entries[label], "get") else entries[label].get()
            if not val and label in ["Họ tên", "Tên KH", "Tên SP"]:
                messagebox.showwarning("Lỗi", f"Không được để trống {label.lower()}!")
                return
            values.append(val if val else None)
            update_cols.append(f"{cols[labels.index(label)]}=%s")

        conn = connect_db()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute(f"UPDATE {table} SET {','.join(update_cols)} WHERE {cols[0]}=%s", values + [ma])
                conn.commit()
                messagebox.showinfo("Thành công", f"Đã cập nhật {ma}")
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi CSDL", f"Không sửa được: {e}")
            finally:
                cur.close()
                conn.close()
            load_data()
            clear_form()

    def xoa():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Lỗi", "Chọn dòng để xóa!")
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa?"):
            ma = tree.item(selected[0])['values'][0]
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute(f"DELETE FROM {table} WHERE {cols[0]}=%s", (ma,))
                    conn.commit()
                    messagebox.showinfo("Thành công", f"Đã xóa {ma}")
                except mysql.connector.Error as e:
                    messagebox.showerror("Lỗi CSDL", f"Không xóa được: {e}")
                finally:
                    cur.close()
                    conn.close()
                load_data()
                clear_form()

    def chon_dong(event):
        selected = tree.selection()
        if not selected: return
        values = tree.item(selected[0])['values']
        clear_form()
        for i, val in enumerate(values):
            label = labels[i]
            if label in ["Mã NV", "Mã SP", "Mã KH"]:
                entries[label].config(state="normal"); entries[label].delete(0, tk.END); entries[label].insert(0, val); entries[label].config(state="readonly")
            elif label in ["Giới tính", "Chức vụ"]:
                try: entries[label].set(val)
                except: pass
            else:
                entries[label].delete(0, tk.END); entries[label].insert(0, str(val) if val is not None else "")

    def clear_form():
        for label, e in entries.items():
            if label in ["Mã NV", "Mã SP", "Mã KH"]:
                try: e.config(state="normal"); e.delete(0, tk.END); e.config(state="readonly")
                except: pass
                continue
            if hasattr(e, "delete"): e.delete(0, tk.END)
            elif hasattr(e, "set"):
                default = "Nam" if "Giới tính" in label else "Nhân Viên Bán Hàng" if "Chức vụ" in label else "0"
                e.set(default)
            if label == "Tồn kho": e.insert(0, "0")

    btn_frame = tk.Frame(win, bg="#f0f2f5")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="THÊM", bg="#27ae60", fg="white", command=them, width=15).pack(side="left", padx=10)
    tk.Button(btn_frame, text="SỬA", bg="#f39c12", fg="white", command=sua, width=15).pack(side="left", padx=10)
    tk.Button(btn_frame, text="XÓA", bg="#e74c3c", fg="white", command=xoa, width=15).pack(side="left", padx=10)
    tk.Button(btn_frame, text="LÀM MỚI", bg="#95a5a6", fg="white", command=clear_form, width=15).pack(side="left", padx=10)
    tk.Button(btn_frame, text="QUAY LẠI", bg="#34495e", fg="white", command=lambda: [win.destroy(), open_main_window()], width=15).pack(side="right", padx=20)

    tree.bind("<<TreeviewSelect>>", chon_dong)
    load_data()
    win.mainloop()
# ====================== TẠO MÃ HÓA ĐƠN DUY NHẤT ======================
def generate_ma_hd():
    try:
        conn = connect_db()
        if not conn:
            return None
        with conn:
            with conn.cursor() as cur:
                today = datetime.now().strftime('%Y%m%d')
                prefix = f"HD{today}"
                cur.execute("""
                    SELECT ma_hd FROM HoaDon 
                    WHERE ma_hd LIKE %s 
                    ORDER BY ma_hd DESC LIMIT 1
                """, (f"{prefix}%",))
                last = cur.fetchone()
                if last:
                    new_num = int(last[0][10:]) + 1
                else:
                    new_num = 100
                return f"{prefix}{new_num}"
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không tạo mã HD: {e}")
        return None
# ====================== BÁN HÀNG – IN HÓA ĐƠN TXT ======================
def open_sales_window(prev):
    prev.destroy()
    root = tk.Tk()
    root.title("BÁN HÀNG - POS")
    root.geometry("1400x800")
    center_window(root, 1400, 800)
    root.configure(bg="#f0f2f5")

    tk.Label(root, text="GIAO DIỆN BÁN HÀNG", font=("Time New Roman", 26, "bold"), bg="#f0f2f5", fg="#2c3e50").pack(pady=15)

    info_frame = tk.LabelFrame(root, text=" THÔNG TIN HÓA ĐƠN ", font=("Time New Roman", 14, "bold"), bg="white", bd=2)
    info_frame.pack(pady=10, padx=20, fill="x")

    tk.Label(info_frame, text="Mã HD:", bg="white").grid(row=0, column=0, padx=10, pady=8, sticky="w")

    ma_hd = generate_ma_hd()
    if not ma_hd:
        messagebox.showerror("Lỗi", "Không thể tạo mã hóa đơn! Vui lòng kiểm tra kết nối CSDL.")
        root.destroy()
        open_main_window()
        return

    lbl_ma_hd = tk.Label(info_frame, text=ma_hd, font=("Time New Roman", 12, "bold"), bg="white", fg="#e74c3c")
    lbl_ma_hd.grid(row=0, column=1, sticky="w")


    tk.Label(info_frame, text="Nhân viên:", bg="white").grid(row=0, column=2, padx=20, sticky="w")
    cbb_nv = ttk.Combobox(info_frame, width=30, state="readonly")
    cbb_nv.grid(row=0, column=3, padx=10)

    tk.Label(info_frame, text="Khách hàng:", bg="white").grid(row=1, column=0, padx=10, pady=8, sticky="w")
    kh_frame = tk.Frame(info_frame, bg="white")
    kh_frame.grid(row=1, column=1, columnspan=3, sticky="w", padx=10)
    entry_kh_ten = tk.Entry(kh_frame, width=25)
    entry_kh_ten.pack(side="left")
    entry_kh_ten.insert(0, "Khách lẻ")
    cbb_kh = ttk.Combobox(kh_frame, width=35, state="readonly")
    cbb_kh.pack(side="left", padx=(5,0))

    def load_nvk():
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT ma_nv, ten_nv FROM NhanVien")
                rows = cur.fetchall()
                cbb_nv['values'] = [f"{r[0]} - {r[1]}" for r in rows]
                if rows: cbb_nv.current(0)
                cur.execute("SELECT ma_kh, ten_kh FROM KhachHang")
                kh_rows = cur.fetchall()
                cbb_kh['values'] = [f"{r[0]} - {r[1]}" for r in kh_rows]
            finally:
                cur.close()
                conn.close()
    load_nvk()

    sp_frame = tk.LabelFrame(root, text=" CHỌN SẢN PHẨM ", font=("Time New Roman", 14, "bold"), bg="white", bd=2)
    sp_frame.pack(pady=10, padx=20, fill="x")
    tk.Label(sp_frame, text="Tên SP:", bg="white").grid(row=0, column=0, padx=10, pady=8)
    cbb_sp = ttk.Combobox(sp_frame, width=60, state="readonly")
    cbb_sp.grid(row=0, column=1, padx=10)
    tk.Label(sp_frame, text="SL:", bg="white").grid(row=0, column=2, padx=10)
    entry_sl = tk.Entry(sp_frame, width=8)
    entry_sl.grid(row=0, column=3, padx=10)
    entry_sl.insert(0, "1")

    def load_sp():
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT ma_sp, ten_sp, gia, so_luong_ton FROM SanPham WHERE so_luong_ton > 0")
                rows = cur.fetchall()
                cbb_sp['values'] = [f"{r[0]} - {r[1]} | Giá: {r[2]:,.0f} | Tồn: {r[3]}" for r in rows]
            finally:
                cur.close()
                conn.close()
    load_sp()

    cols = ("STT", "Mã SP", "Tên SP", "SL", "Đơn giá", "Thành tiền")
    tree = ttk.Treeview(root, columns=cols, show="headings", height=12)
    for i, c in enumerate(cols):
        tree.heading(c, text=c)
        tree.column(c, width=80 if i == 0 else 150 if i == 1 else 300 if i == 2 else 100, anchor="center")
    tree.pack(pady=10, padx=20, fill="both", expand=True)

    total = 0
    cart = []

    def add_sp():
        nonlocal total
        sel = cbb_sp.current()
        if sel == -1: return messagebox.showwarning("Lỗi", "Chọn sản phẩm!")
        try: sl = int(entry_sl.get())
        except: return messagebox.showwarning("Lỗi", "Số lượng phải là số!")
        if sl <= 0: return messagebox.showwarning("Lỗi", "Số lượng phải > 0!")

        sp_info = cbb_sp['values'][sel].split(" | ")
        ma_sp = sp_info[0].split(" - ")[0]
        ten_sp = sp_info[0].split(" - ", 1)[1]
        gia = float(sp_info[1].split(": ")[1].replace(",", ""))
        ton = int(sp_info[2].split(": ")[1])
        if sl > ton: return messagebox.showwarning("Lỗi", f"Chỉ còn {ton} sản phẩm!")

        # TÌM VÀ CỘNG DỒN NẾU ĐÃ CÓ
        found = False
        for item in cart:
            if item["ma_sp"] == ma_sp:
                item["sl"] += sl
                item["sub"] = item["gia"] * item["sl"]
                found = True
                break

        if not found:
            sub = gia * sl
            cart.append({"ma_sp": ma_sp, "ten": ten_sp, "sl": sl, "gia": gia, "sub": sub})

        # CẬP NHẬT TỔNG TIỀN
        total = sum(item["sub"] for item in cart)

        update_cart()
        entry_sl.delete(0, tk.END); entry_sl.insert(0, "1"); load_sp()
    def update_cart():
        for i in tree.get_children(): tree.delete(i)
        for i, item in enumerate(cart, 1):
            tree.insert("", "end", values=(i, item["ma_sp"], item["ten"], item["sl"], f"{item['gia']:,.0f}", f"{item['sub']:,.0f}"))
        lbl_total.config(text=f"TỔNG TIỀN: {total:,.0f} VND")

    def delete_item():
        selected = tree.selection()
        if not selected: return messagebox.showwarning("Lỗi", "Chọn sản phẩm để xóa!")
        index = tree.index(selected[0])
        removed = cart.pop(index)
        nonlocal total
        total -= removed["sub"]
        update_cart()

    btn_sp_frame = tk.Frame(sp_frame, bg="white")
    btn_sp_frame.grid(row=0, column=5, padx=20)
    tk.Button(btn_sp_frame, text="THÊM", bg="#3498db", fg="white", command=add_sp, width=12).pack(pady=2)
    tk.Button(btn_sp_frame, text="XÓA", bg="#e74c3c", fg="white", command=delete_item, width=12).pack(pady=2)

    lbl_total = tk.Label(root, text="TỔNG TIỀN: 0 VND", font=("Time New Roman", 18, "bold"), bg="#f0f2f5", fg="#e74c3c")
    lbl_total.pack(pady=10)

    def in_hoa_don():
        nonlocal total, cart
        if not cart:
            messagebox.showwarning("Rỗng", "Chưa có sản phẩm để in!")
            return

        ten_kh = entry_kh_ten.get().strip() or "Khách lẻ"
        ma_kh = None
        if cbb_kh.get():
            ma_kh = cbb_kh.get().split(" - ")[0]
        else:
            conn = connect_db()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("SELECT ma_kh FROM KhachHang ORDER BY ma_kh DESC LIMIT 1")
                    last = cur.fetchone()
                    new_id = f"KH{int(last[0][2:]) + 1:04d}" if last and last[0] else "KH0001"
                    cur.execute("INSERT INTO KhachHang (ma_kh, ten_kh) VALUES (%s, %s)", (new_id, ten_kh))
                    ma_kh = new_id
                    conn.commit()
                    load_nvk()
                except mysql.connector.Error as e:
                    messagebox.showerror("Lỗi CSDL", f"Không thêm khách hàng: {e}")
                    return
                finally:
                    cur.close()
                    conn.close()

        if not cbb_nv.get():
            messagebox.showwarning("Lỗi", "Chọn nhân viên!")
            return
        nv_info = cbb_nv.get()
        ma_nv = nv_info.split(" - ")[0]
        ten_nv = nv_info.split(" - ", 1)[1]

        ma_hd_moi = generate_ma_hd()
        if not ma_hd_moi:
            messagebox.showerror("Lỗi", "Không thể tạo mã hóa đơn mới!")
            return

        in_hoa_don_txt(
            ma_hd=ma_hd_moi,
            ngay_lap=datetime.now().strftime("%d/%m/%Y %H:%M"),
            ma_nv=ma_nv,
            ten_nv=ten_nv,
            ma_kh=ma_kh,
            ten_kh=ten_kh,
            cart=cart,
            tong_tien=total
        )

        conn = connect_db()
        if not conn:
            return

        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO HoaDon (ma_hd, ma_kh, ma_nv, ngay_lap, tong_tien)
                VALUES (%s, %s, %s, %s, %s)
            """, (ma_hd_moi, ma_kh, ma_nv, datetime.now().date(), total))

            for item in cart:
                cur.execute("""
                    INSERT INTO ChiTietHoaDon (ma_hd, ma_sp, so_luong, don_gia)
                    VALUES (%s, %s, %s, %s)
                """, (ma_hd_moi, item["ma_sp"], item["sl"], item["gia"]))
                cur.execute("""
                    UPDATE SanPham SET so_luong_ton = so_luong_ton - %s
                    WHERE ma_sp = %s
                """, (item["sl"], item["ma_sp"]))

            conn.commit()
            messagebox.showinfo("HOÀN TẤT", f"Đã in hóa đơn!\nMã HD: {ma_hd_moi}")
            lbl_ma_hd.config(text=ma_hd_moi)
            reset()
        except mysql.connector.Error as e:
            conn.rollback()
            messagebox.showerror("Lỗi CSDL", f"Lưu thất bại: {e}")
        finally:
            cur.close()
            conn.close()
    def reset():
        nonlocal total, cart
        cart.clear(); update_cart()
        total = 0
        entry_sl.delete(0, tk.END); entry_sl.insert(0, "1")
        entry_kh_ten.delete(0, tk.END); entry_kh_ten.insert(0, "Khách lẻ")
        load_sp()

    btn_f = tk.Frame(root, bg="#f0f2f5")
    btn_f.pack(pady=20)
    tk.Button(btn_f, text="LÀM MỚI", bg="#95a5a6", fg="white", command=reset, width=15).pack(side="left", padx=20)
    tk.Button(btn_f, text="QUAY LẠI", bg="#e74c3c", fg="white", command=lambda: [root.destroy(), open_main_window()], width=15).pack(side="left", padx=10)
    tk.Button(btn_f, text="IN HÓA ĐƠN", font=("Time New Roman", 14, "bold"), bg="#27ae60", fg="white", width=22, height=2, command=in_hoa_don).pack(side="right", padx=40)

    root.mainloop()

# ====================== CHẠY CHƯƠNG TRÌNH ======================
if __name__ == "__main__":

    create_login_window()
